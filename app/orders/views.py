import os
from datetime import datetime, timedelta, timezone
from app.orders.permissions import IsOrderFileDataOwnerWithoutUser

from app.utils import errorcode
from app.utils.decorators import check_file_type, check_user_quota
from app.utils.errorcode import NotAllowedUser, QuestionnaireTypeIdNotFound
from app.utils.storage import CloudStorage, ServerFileSystem

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


from .models import STATE_CHOICES, FileData, OrderFileData, OrderModel, OrderOffer
from .permissions import IsOrderOwner

from .serializers import AllOrdersClientSerializer, OrderOfferSerializer
from .swagger_documentation.orders import (
    AllOrdersClientGetList,
    ArchiveOrdersClientGetList,
    FileOrderGet,
    OfferCreate,
    OfferGetList,
    UploadImageOrderPost,
    FileOrderDelete,
    OrderCreate,
    QuestionnaireResponsePost,
    QuestionnaireResponseGet,

)
from .tasks import celery_delete_file_task, celery_delete_image_task, celery_upload_file_task, celery_upload_image_task
from app.products.models import Category
from app.main_page.permissions import IsContractor
from app.questionnaire.models import QuestionnaireType, Question, QuestionResponse
from app.questionnaire.serializers import QuestionnaireResponseSerializer, OrderFullSerializer

IMAGE_FILE_FORMATS = ["jpg", "gif", "jpeg", ]


@swagger_auto_schema(
        operation_description=OrderCreate.operation_description,
        request_body=OrderCreate.request_body,
        responses=OrderCreate.responses,
        method = "POST"
    )
@api_view(["POST"])
@permission_classes([AllowAny])
def create_order(request):

    """ Создание заказа клиента """
    if "order_name" in request.data:
        order_name = request.data.get("order_name")
    else:
        order_name = f"Заказ №{1 if not OrderModel.objects.last() else OrderModel.objects.last().id + 1}"
    order_description = request.data.get("order_description")
    order_questionnaire_type = request.data.get("questionnaire_type_id")

    if QuestionnaireType.objects.filter(id=order_questionnaire_type).exists() is False:
        raise QuestionnaireTypeIdNotFound
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    order = OrderModel.objects.create(
        user_account=user,
        name=order_name,
        questionnaire_type=QuestionnaireType.objects.get(id=order_questionnaire_type),
    )
    if order_description:
        order.order_description = order_description
        order.save()
    response = Response({'success': 'the order was created',
                         "order_id": order.id,
                         }, status=201)
    if not user:
        response.set_cookie("key", order.key, samesite="None", secure=True)
    return response


class OrderOfferViewSet(viewsets.ModelViewSet):
    """Поведение Оффера"""
    serializer_class = OrderOfferSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action == 'list':
            # уточнить пермишены
            permission_classes = [IsAuthenticated, ]
        if self.action == 'create':
            # уточнить пермишены
            permission_classes = [IsAuthenticated, IsContractor, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        order_id = self.kwargs['pk']
        if OrderModel.objects.filter(id=order_id).exists():
            date = OrderModel.objects.get(id=order_id).order_time
            if (datetime.now(timezone.utc) - date) > timedelta(hours=24):
                return OrderOffer.objects.filter(order_id=order_id).all()
        return []

    @swagger_auto_schema(
        operation_description=OfferGetList.operation_description,
        responses=OfferGetList.responses
    )
    def list(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        if not OrderModel.objects.filter(id=order_id).exists():
            raise errorcode.OrderIdNotFound()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description=OfferCreate.operation_description,
        request_body=OfferCreate.request_body,
        responses=OfferCreate.responses
    )
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
        return OrderModel.objects.filter(user_account=user).exclude(state="completed")

    @swagger_auto_schema(
        operation_description=AllOrdersClientGetList.operation_description,
        request_body=AllOrdersClientGetList.request_body,
        responses=AllOrdersClientGetList.responses,
        manual_parameters=AllOrdersClientGetList.manual_parameters
    )
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

    @swagger_auto_schema(
        operation_description=ArchiveOrdersClientGetList.operation_description,
        request_body=ArchiveOrdersClientGetList.request_body,
        responses=ArchiveOrdersClientGetList.responses,
        manual_parameters=ArchiveOrdersClientGetList.manual_parameters
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description=UploadImageOrderPost.operation_description,
    request_body=UploadImageOrderPost.request_body,
    responses=UploadImageOrderPost.responses,
    method="post",
)
@api_view(["POST"])
@check_file_type(["image/jpg", "image/gif", "image/jpeg", "application/pdf"])
@check_user_quota
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.data.get("order_id")
    upload_file = request.FILES["upload_file"]
    user_id = request.user.id
    name = upload_file.name
    # create new name for file
    new_name = ServerFileSystem(name, user_id, order_id).generate_new_filename()

    if order_id is None:
        raise errorcode.IncorrectImageOrderUpload()
    if order_id == "" or not order_id.isdigit() or not OrderModel.objects.filter(id=order_id).exists():
        raise errorcode.IncorrectImageOrderUpload()

    # temporary save file
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    with open(f"tmp/{new_name}", "wb+") as file:
        for chunk in upload_file.chunks():
            file.write(chunk)
    temp_file = f"tmp/{new_name}"
    if temp_file.split('.')[-1] in IMAGE_FILE_FORMATS:
        task = celery_upload_image_task.delay(temp_file, user_id, order_id)
    else:
        task = celery_upload_file_task.delay(temp_file, user_id, order_id)
    return Response({"task_id": task.id}, status=202)


@swagger_auto_schema(
    operation_description=FileOrderGet.operation_description,
    responses=FileOrderGet.responses,
    manual_parameters=FileOrderGet.manual_parameters,
    method="get",
)
@api_view(["GET"])
def get_file_order(request, file_id):
    """
    Получение изображения из Yandex и передача ссылки на его получение для фронта
    """
    image_data = get_object_or_404(FileData, id=file_id)
    if request.user.id != image_data.user_account.id:
        raise NotAllowedUser

    yandex_path = image_data.yandex_path

    # get download_url from Yandex
    yandex = CloudStorage()
    try:
        image_data = yandex.cloud_get_image(yandex_path)
    except Exception as e:
        return Response(
            {
                "status": "failed",
                "message": f"Failed to get image from Yandex.Disk: {str(e)}",
            },
        )
    return Response(image_data)





@swagger_auto_schema(
    operation_description=QuestionnaireResponsePost.operation_description,
    request_body=QuestionnaireResponsePost.request_body,
    responses=QuestionnaireResponsePost.responses,
    method="POST"
)
@api_view(["POST"])
@permission_classes([IsOrderOwner])
def create_answers_to_oder(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
    except Exception:
        raise errorcode.OrderIdNotFound()
    serializer = QuestionnaireResponseSerializer(data=request.data, many=True,
                                                 context={"order": order,
                                                          "questionnairetype": order.questionnaire_type})
    serializer.is_valid(raise_exception=True)
    questionnaire_questions = Question.objects.filter(
        chapter__type=order.questionnaire_type)
    questions_id_with_answers = [answer["question_id"] for answer in request.data]
    questions_with_answers = Question.objects.filter(id__in=questions_id_with_answers).all()
    for question in questionnaire_questions:
        if (question.answer_required
                and question.option
                and question not in questions_with_answers
                and {"question_id": question.option.question.id,
                     "response": question.option.text} in request.data
        ):
            raise ValidationError({
                "question_id": f"Вопрос '{question.id}' требует ответа."
            })
    for question in questions_with_answers:
        if question.option and question.option.question not in questions_with_answers:
            raise ValidationError({
                "question_id": f"Вопрос '{question.option.question.id}' требует ответа."
            })
    serializer.save(order=order)
    return Response(serializer.data)


@swagger_auto_schema(
    operation_description=QuestionnaireResponseGet.operation_description,
    responses=QuestionnaireResponseGet.responses,
    method="GET"
)
@api_view(["GET"])
@permission_classes([IsOrderOwner])
def get_answers_to_oder(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
    except Exception:
        raise errorcode.OrderIdNotFound()
    serializer = OrderFullSerializer(order)
    return Response(serializer.data)


class OrderFileAPIView(viewsets.ViewSet, GenericAPIView):

    @swagger_auto_schema(
        operation_description=FileOrderDelete.operation_description,
        responses=FileOrderDelete.responses,
        request_body=FileOrderDelete.request_body,
    )
    @permission_classes([IsOrderFileDataOwnerWithoutUser])
    def delete_file_order(self, request):
        """
        Удаление файла из Yandex и передача ссылки на его получение для фронта
        """
        file_id = request.data.get('file_id')
        try:
            file_to_delete = OrderFileData.objects.get(id=file_id)
            if file_to_delete.original_name.split('.')[-1] in IMAGE_FILE_FORMATS:
                task = celery_delete_image_task.delay(file_id)
            else:
                task = celery_delete_file_task.delay(file_id)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        except OrderFileData.DoesNotExist:
            return Response({"detail": "Файл не найден."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Ошибка: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
