import os
from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, viewsets, views, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, status, viewsets, views
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from django.db.models import Q, Prefetch
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.utils.decorators import method_decorator

from app.orders.permissions import (
    IsOrderFileDataOwnerWithoutUser,
    IsOrderExists,
    IsUserQuotaForClone,
)
from app.questionnaire.models import (
    QuestionnaireType,
    Question,
)
from app.questionnaire.serializers import (
    QuestionnaireResponseSerializer,
    OrderFullSerializer,
)
from app.sending.views import send_user_notifications
from app.users.signals import send_notify
from app.users.utils.quota_manager import UserQuotaManager
from app.main_page.models import ContractorData
from app.main_page.permissions import IsContractor
from app.utils import errorcode
from app.utils.decorators import check_file_type, check_user_quota
from app.utils.file_work import FileWork
from app.utils.storage import ServerFileSystem
from .constants import ErrorMessages, ORDER_STATE_CHOICES
from . import permissions as perm
from .models import OrderFileData, OrderModel, OrderOffer, WorksheetFile
from .serializers import (
    AllOrdersClientSerializer,
    OrderModelSerializer,
    OfferOrderSerializer,
    OfferContactorSerializer,
    OfferSerizalizer,
)
from .swagger_documentation import orders as swagger

from .tasks import celery_copy_order_file_task

from .utils.files import (
    delete_file,
    delete_image,
    upload_file_to_answer,
    upload_image_to_answer,
)
from .utils.services import (
    range_filter,
    last_contactor_key_offer,
    select_offer,
)
from .utils.order_state import OrderStateActivate
from .utils.db_data import CloneOrderDB


@swagger_auto_schema(**swagger.OrderCreate.__dict__)
@api_view(["POST"])
@permission_classes([AllowAny])
def create_order(request):
    """
    Создание заказа клиента.
    URL: http://localhost/order/create/
    METHOD - "POST"
    order_name:str (необязательное) - имя заказа,
    order_description:str (необязательное) - описание заказа,
    questionnaire_type_id:int (обязательное) - id типа анкеты
    """
    if "order_name" in request.data:
        order_name = request.data.get("order_name")
    else:
        order_number = 1
        if OrderModel.objects.last():
            order_number = OrderModel.objects.last().id + 1
        order_name = f"Заказ №{order_number}"
    order_description = request.data.get("order_description")
    order_questionnaire_type = request.data.get("questionnaire_type_id")

    if (
        QuestionnaireType.objects.filter(id=order_questionnaire_type).exists()
        is False
    ):
        raise errorcode.QuestionnaireTypeIdNotFound
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    order = OrderModel.objects.create(
        user_account=user,
        name=order_name,
        questionnaire_type=QuestionnaireType.objects.get(
            id=order_questionnaire_type
        ),
    )
    if order_description:
        order.order_description = order_description
        order.save()
    response = Response(
        {
            "success": "the order was created",
            "order_id": order.id,
        },
        status=201,
    )
    if not user:
        response.set_cookie(
            settings.ORDER_COOKIE_KEY_NAME,
            order.key,
            samesite="None",
            secure=True,
        )
    else:
        context = {"order_id": order.id, "user_id": user.id}
        if user.notifications:
            send_user_notifications(
                user,
                "ORDER_CREATE_CONFIRMATION",
                context,
                [
                    user.email,
                ],
            )
    return response


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(**swagger.OrderOfferList.__dict__),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(**swagger.OrderOfferCreate.__dict__),
)
class OfferViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Операции с офферами
    """

    queryset = OrderOffer.objects.all()
    serializer_class = OfferSerizalizer
    permission_classes = (IsAuthenticated, IsContractor)

    def get_queryset(self):
        user = self.request.user
        return OrderOffer.objects.filter(user_account=user)

    def get_permissions(self):
        if self.action == "create":
            return [
                IsAuthenticated(),
                IsContractor(),
                perm.OneOfferPerContactor(),
            ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contactor_key = (
            last_contactor_key_offer(request.data.get("order_id")) + 1
        )
        serializer.validated_data.update(
            {"contactor_key": contactor_key, "user_account": request.user}
        )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # @action(
    #     methods=["post"],
    #     detail=True,
    #     url_path="select",
    #     permission_classes=[IsAuthenticated, perm.IsOrderOfferStateNotDraft],
    # )
    # def select_offer_view(self, request, *args, **kwargs):
    #     """
    #     Меняет статус оффера на выбран,
    #     статус на заказа на выбран,
    #     остальные офферы заказа на отклонен
    #     """
    #     instance = self.get_object()
    #     select_offer(instance)
    #     serializer = OfferSerizalizer(instance=instance, many=False)
    #     return Response(data=serializer.data)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(**swagger.AllOffersToOrder.__dict__),
)
class OrderOfferView(generics.ListAPIView):
    """Офферы по заказу"""

    serializer_class = OfferOrderSerializer
    permission_classes = [
        IsAuthenticated,
        perm.IsOrderOwner,
    ]

    def get_queryset(self):
        order_id = self.kwargs.get("pk")
        offers = (
            OrderOffer.objects.filter(
                order_id=order_id,
                order_id__order_time__lt=range_filter(
                    settings.OFFER_ACCESS_HOURS
                ),
            )
            .select_related("order_id", "chat", "user_account__contractordata")
            .prefetch_related(
                Prefetch(lookup="order_id__orderfiledata_set", to_attr="files")
            )
            .only(
                "id",
                "user_account_id",
                "order_id_id",
                "offer_price",
                "offer_execution_time",
                "offer_description",
                "contactor_key",
                "status",
                "user_account__id",
                "user_account__contractordata__user_id",
                "user_account__contractordata__company_name",
                "order_id__id",
                "chat__id",
            )
            .all()
        )
        return offers


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(**swagger.ContactorOffer.__dict__),
)
class ContactorOfferView(generics.ListAPIView):
    """
    Офферы исполнителя
    """

    serializer_class = OfferContactorSerializer
    permission_classes = [
        IsAuthenticated,
        IsContractor,
    ]

    def get_queryset(self):
        # прячем ошибку swagger
        if getattr(self, "swagger_fake_view", False):
            return OrderOffer.objects.none()
        contactor_id = self.kwargs.get("pk")
        contactor = (
            ContractorData.objects.filter(pk=contactor_id)
            .only("user_id")
            .first()
        )
        offers = (
            OrderOffer.objects.filter(user_account_id=contactor.user_id)
            .select_related("order_id", "chat")
            .only(
                "id",
                "user_account_id",
                "order_id_id",
                "offer_price",
                "offer_execution_time",
                "offer_description",
                "contactor_key",
                "status",
                "order_id__id",
                "order_id__name",
                "chat__id",
            )
            .all()
        )
        return offers


class AllOrdersClientViewSet(viewsets.ModelViewSet):
    """Поведение Заказа для отображения в личном кабинете."""

    queryset = OrderModel.objects.all()
    serializer_class = AllOrdersClientSerializer

    # достаем все заказы пользователя, кроме выполненных
    def get_queryset(self):
        user = self.request.user
        return OrderModel.objects.filter(
            Q(user_account=user),
            Q(state=ORDER_STATE_CHOICES[2][0])
            | Q(state=ORDER_STATE_CHOICES[1][0]),
        )

    @swagger_auto_schema(**swagger.AllOrdersClientGetList.__dict__)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArchiveOrdersClientViewSet(viewsets.ModelViewSet):
    """Получение списка архивных заказов клиента."""

    queryset = OrderModel.objects.all()
    serializer_class = AllOrdersClientSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderModel.objects.filter(user_account=user, state="completed")

    @swagger_auto_schema(**swagger.ArchiveOrdersClientGetList.__dict__)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@swagger_auto_schema(**swagger.QuestionnaireResponsePost.__dict__)
@api_view(["POST"])
@permission_classes([perm.IsOrderOwner])
def create_answers_to_order(request, pk):
    """
    Создание ответов на вопросы к заказу.
    URL: http://localhost/order/<int:pk>/answers/
    METHOD - "POST"
    param pk:int (обязательное) - id заказа,
    question_id:int (обязательное) - id вопроса,
    response:str (обязательное) - ответ на вопрос
    """

    try:
        order = OrderModel.objects.get(id=pk)
    except Exception:
        raise errorcode.OrderIdNotFound()
    serializer = QuestionnaireResponseSerializer(
        data=request.data,
        many=True,
        context={
            "order": order,
            "questionnairetype": order.questionnaire_type,
        },
    )
    serializer.is_valid(raise_exception=True)
    questionnaire_questions = Question.objects.filter(
        chapter__type=order.questionnaire_type
    )
    questions_id_with_answers = [
        answer["question_id"] for answer in request.data
    ]
    questions_with_answers = Question.objects.filter(
        id__in=questions_id_with_answers
    ).all()
    for question in questionnaire_questions:
        if (
            question.answer_required
            and question.option
            and question not in questions_with_answers
            and {
                "question_id": question.option.question.id,
                "response": question.option.text,
            }
            in request.data
        ):
            raise ValidationError(
                {
                    "question_id": ErrorMessages.QUESTION_ANSWER_REQUIRED.format(
                        {question.id}
                    )
                }
            )
    for question in questions_with_answers:
        if (
            question.option
            and question.option.question not in questions_with_answers
        ):
            raise ValidationError(
                {
                    "question_id": ErrorMessages.QUESTION_ANSWER_REQUIRED.format(
                        question.option.question.id
                    )
                }
            )
    serializer.save(order=order)
    return Response(serializer.data)


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(**swagger.QuestionnaireResponseGet.__dict__),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(**swagger.OrderUpdate.__dict__),
)
class OrderViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = OrderModel.objects.all()
    serializer_class = OrderFullSerializer
    permission_classes = [
        perm.IsOrderOwner,
    ]


@permission_classes([IsAuthenticated])
def get_answers_to_last_order(request):
    """
    Получение ответов на вопросы к последнему заказу в статусе черновика.
    URL: http://localhost/order/last/
    METHOD - "GET"
    """
    user = request.user
    order = OrderModel.objects.filter(
        user_account=user, state=ORDER_STATE_CHOICES[0][0]
    ).last()
    if not order:
        raise errorcode.OrderIdNotFound()
    serializer = OrderFullSerializer(order)
    return Response(serializer.data)


@swagger_auto_schema(**swagger.FileOrderDelete.__dict__)
@api_view(["DELETE"])
@permission_classes([IsOrderFileDataOwnerWithoutUser])
def delete_file_order(request):
    """
    Удаление файла из Yandex и превью с сервера
    URL: http://localhost/order/file_order/
    METHOD - "DELETE"
    file_id: int - id файла (модели OrderFileData) привязанного к вопросу
    анкеты
    """
    file_id = request.data.get("file_id")
    try:
        file_to_delete = OrderFileData.objects.get(id=file_id)
        if request.user.is_authenticated:
            quota_manager = UserQuotaManager(request.user)
        else:
            quota_manager = None
        if (
            file_to_delete.original_name.split(".")[-1]
            in settings.IMAGE_FILE_FORMATS
        ):
            # task = celery_delete_image_task.delay(file_id)
            response = delete_image(file_id, quota_manager)
        else:
            # task = celery_delete_file_task.delay(file_id)
            response = delete_file(file_id, quota_manager)
        return response
    except OrderFileData.DoesNotExist:
        return Response(
            {"detail": ErrorMessages.FILE_NOT_FOUNDED},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"detail": f"Ошибка: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(**swagger.AttachFileAnswerPost.__dict__)
@api_view(["POST"])
@permission_classes([perm.IsOrderOwner])
@parser_classes([MultiPartParser])
@check_file_type(["image/jpg", "image/gif", "image/jpeg", "application/pdf"])
@check_user_quota
def attach_file(request, pk: int):
    """
    Добавление файла к определенному вопросу заказа.
    URL: http://localhost/order/<int:pk>/files/
    METHOD - "POST"
    pk:int (обязательное) - id заказа к которому крепится файл,
    Данные которые передаются через form-data
        - question_id: int (обязательное) - id вопроса к которому
        прилагается файл или изображение,
        - upload_file (обязательное) - файл или изображение, отправляемые пользователем,
        передается через request.FILES
    """
    order_id = pk
    question_id = request.data.get("question_id")
    try:
        order = OrderModel.objects.get(id=order_id)
        Question.objects.get(
            id=question_id, chapter__type=order.questionnaire_type
        )
    except OrderModel.DoesNotExist:
        raise errorcode.OrderIdNotFound()
    except Question.DoesNotExist:
        raise errorcode.QuestionIdNotFound()
    if "upload_file" not in request.FILES:
        raise ValidationError({"detail": ErrorMessages.FILE_NOT_FOUNDED})
    upload_file = request.FILES["upload_file"]
    original_name = upload_file.name

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None

    new_name = ServerFileSystem(original_name, user_id, order_id).filename

    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    with open(f"tmp/{new_name}", "wb+") as file:
        for chunk in upload_file.chunks():
            file.write(chunk)
    temp_file = f"tmp/{new_name}"
    if request.user.is_authenticated:
        quota_manager = UserQuotaManager(request.user)
    else:
        quota_manager = None
    if temp_file.split(".")[-1] in settings.IMAGE_FILE_FORMATS:
        # task = celery_upload_image_task_to_answer.delay(
        #     temp_file, order_id, user_id, question_id, original_name
        # )
        response = upload_image_to_answer(
            temp_file,
            order_id,
            question_id,
            original_name,
            quota_manager,
            user_id=user_id,
        )
    else:
        # task = celery_upload_file_task_to_answer.delay(
        #     temp_file, order.id, user_id, question_id, original_name
        # )
        response = upload_file_to_answer(
            temp_file,
            order.id,
            question_id,
            original_name,
            quota_manager,
            user_id=user_id,
        )

    return response


@swagger_auto_schema(**swagger.FileOrderDownload.__dict__)
@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_download_file_link(request, file_id) -> Any:
    """
    Получение и передача на фронт ссылки на скачивание файла
    URL: http://localhost/download/
    METHOD - "GET"
    file_id:str (обязательное) - id файла,
    """

    try:
        UUID(str(file_id))
    except ValueError:
        raise errorcode.FileNotFound()
    file_models = (OrderFileData, WorksheetFile)
    file = None
    for file_model in file_models:
        file = file_model.objects.filter(id=file_id.strip()).first()
        if file:
            break
    if not file:
        raise errorcode.FileNotFound()
    try:
        file_link = FileWork.get_download_file_link(file)
    except Exception as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    return HttpResponsePermanentRedirect(file_link)


class OrderStateActivateView(views.APIView):
    """
    Активирует заказ меняя его статус на offer
    """

    permission_classes = (IsAuthenticated, perm.IsOrderOwner)

    def get_object(self) -> OrderModel:
        instance = OrderModel.objects.filter(pk=self.kwargs.get("pk")).first()
        return instance

    def serialize(self, instance: OrderModel):
        serializer = OrderModelSerializer(instance=instance)
        return serializer.data

    @swagger_auto_schema(**swagger.OrderStateActivateSwagger.__dict__)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        OrderStateActivate(instance).execute()
        send_notify.send(
            sender=self.__class__, user=instance.user_account, order=instance
        )

        data = self.serialize(instance)
        return Response(data=data, status=200)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(**swagger.CloneOrderCreate.__dict__),
)
class CloneOrderView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (
        IsAuthenticated,
        IsOrderExists,
        perm.IsOrderOwner,
        IsUserQuotaForClone,
    )

    def create(self, request, *args, **kwargs):
        """
        Клонирование заказа со всеми связанными данными.
        URL: http://localhost/order/clone/
        METHOD - "POST"
        Данные передаваемые в запросе:
            - order_id: int - id заказа который необходимо клонировать,
        @return: Response object {"new_order_id": int}
        """
        old_order_id = request.data.get("order_id")
        user_id = OrderModel.objects.get(pk=old_order_id).user_account.pk

        db = CloneOrderDB(user_id=user_id, old_order_id=old_order_id)
        db.clone_order()
        db.clone_order_question_response()
        state_copy = db.clone_order_file_data()

        if state_copy:
            celery_copy_order_file_task.delay(
                user_id, old_order_id, db.order_id
            )

        return Response(
            {"order_id": db.order_id}, status=status.HTTP_201_CREATED
        )


@swagger_auto_schema(**swagger.AcceptOffer.__dict__)
@api_view(["POST"])
@permission_classes([perm.IsOrderOwner, perm.IsOrderOfferStateIsOffer])
def accept_offer(request, pk):
    """
    Меняет статус оффера на выбран,
    статус на заказа на выбран,
    остальные офферы заказа на отклонен
    """
    offer_id = request.data.get("offer_id")
    if not offer_id:
        raise errorcode.OfferNotFound()
    offer = OrderOffer.objects.filter(id=offer_id).first()
    if not offer:
        raise errorcode.OfferNotFound()
    if offer.order_id.id != pk:
        raise errorcode.IncorrectOffer()
    selected_offer = select_offer(offer)
    serializer = OfferSerizalizer(instance=selected_offer, many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
