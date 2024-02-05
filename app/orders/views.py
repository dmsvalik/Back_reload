import os
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from django.http import HttpResponsePermanentRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets, views
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from django.db.models import Q
from django.utils.decorators import method_decorator

from app.main_page.permissions import IsContractor
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
from app.utils import errorcode
from app.utils.decorators import check_file_type, check_user_quota
from app.utils.errorcode import QuestionnaireTypeIdNotFound
from app.utils.file_work import FileWork
from app.utils.storage import ServerFileSystem
from config.settings import IMAGE_FILE_FORMATS, ORDER_COOKIE_KEY_NAME
from .constants import ErrorMessages, ORDER_STATE_CHOICES
from .models import OrderFileData, OrderModel, OrderOffer, WorksheetFile
from .permissions import IsOrderOwner
from .serializers import (
    AllOrdersClientSerializer,
    OrderOfferSerializer,
    OrderModelSerializer,
)
from .swagger_documentation import orders as swagger

from .tasks import celery_copy_order_file_task

#     celery_delete_file_task,
#     celery_delete_image_task,
#     celery_upload_file_task_to_answer,
#     celery_upload_image_task_to_answer,
# )
from .utils.files import (
    delete_file,
    delete_image,
    upload_file_to_answer,
    upload_image_to_answer,
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
        raise QuestionnaireTypeIdNotFound
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
            ORDER_COOKIE_KEY_NAME, order.key, samesite="None", secure=True
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
    name="retrieve",
    decorator=swagger_auto_schema(**swagger.OrderOfferRetrieve.__dict__),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(**swagger.OrderOfferDelete.__dict__),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(**swagger.OrderOfferUpdate.__dict__),
)
class OrderOfferViewSet(viewsets.ModelViewSet):
    """Поведение Оффера"""

    serializer_class = OrderOfferSerializer

    def get_permissions(self):
        permission_classes = [
            IsAuthenticated,
        ]
        if self.action == "list":
            # уточнить пермишены
            permission_classes = [
                IsAuthenticated,
            ]
        if self.action == "create":
            # уточнить пермишены
            permission_classes = [
                IsAuthenticated,
                IsContractor,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        order_id = self.kwargs.get("pk", None)
        if OrderModel.objects.filter(id=order_id).exists():
            date = OrderModel.objects.get(id=order_id).order_time
            if (datetime.now(timezone.utc) - date) > timedelta(hours=24):
                return OrderOffer.objects.filter(order_id=order_id).all()
        return []

    @swagger_auto_schema(**swagger.OfferGetList.__dict__)
    def list(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        if not OrderModel.objects.filter(id=order_id).exists():
            raise errorcode.OrderIdNotFound()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**swagger.OfferCreate.__dict__)
    def create(self, request, *args, **kwargs):
        return super().create(request)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.is_valid()
        serializer.save(user_account=user)


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
@permission_classes([IsOrderOwner])
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
        IsOrderOwner,
    ]


@swagger_auto_schema(**swagger.QuestionnaireResponseLastGet.__dict__)
@api_view(["GET"])
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
        if file_to_delete.original_name.split(".")[-1] in IMAGE_FILE_FORMATS:
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
@permission_classes([IsOrderOwner])
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
    if temp_file.split(".")[-1] in IMAGE_FILE_FORMATS:
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

    permission_classes = (IsAuthenticated, IsOrderOwner)

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
class CloneOrderView(CreateAPIView):
    serializer_class = None
    permission_classes = (
        IsAuthenticated,
        IsOrderExists,
        IsOrderOwner,
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
