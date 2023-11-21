import os
from datetime import datetime, timedelta, timezone

from app.utils import errorcode
from app.utils.decorators import check_file_type, check_user_quota
from app.utils.errorcode import CategoryIdNotFound, IncorrectPostParameters, NotAllowedUser
from app.utils.storage import CloudStorage, ServerFileSystem

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import STATE_CHOICES, FileData, OrderModel, OrderOffer
from .serializers import AllOrdersClientSerializer, OrderOfferSerializer
from .swagger_documentation.orders import (
    AllOrdersClientGetList,
    ArchiveOrdersClientGetList,
    FileOrderGet,
    OfferCreate,
    OfferGetList,
    UploadImageOrderPost,
)
from .tasks import celery_upload_file_task, celery_upload_image_task
from app.products.models import Category
from app.main_page.permissions import IsContractor

IMAGE_FILE_FORMATS = ["jpg", "gif", "jpeg", ]


@api_view(["POST"])
def create_order(request):

    """ Создание заказа клиента """

    order_name = request.data.get("order_name")
    order_description = request.data.get("order_description")
    order_category = request.data.get("order_category")
    order_state = request.data.get("order_state", default='draft')

    if order_name is None or order_description is None or order_category is None or order_name not in STATE_CHOICES:
        raise IncorrectPostParameters

    if Category.objects.filter(id=order_category).exists() is False:
        raise CategoryIdNotFound

    OrderModel.objects.create(
        user_account=request.user,
        order_time=datetime.now(tz=timezone.utc),
        name=order_name,
        order_description=order_description,
        card_category=Category.objects.get(id=order_category),
        state=order_state
    )

    return Response({'success': 'the order was created'})


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
