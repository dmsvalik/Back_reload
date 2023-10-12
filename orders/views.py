import os
from datetime import datetime, timedelta, timezone

from utils import errorcode
from utils.decorators import check_file_type, check_user_quota
from utils.errorcode import NotAllowedUser
from utils.storage import CloudStorage, ServerFileSystem

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FileData, OrderModel, OrderOffer
from .permissions import ChangePriceInOrder
from .serializers import OrderModelMinifieldSerializer, OrderOfferSerializer
from .tasks import celery_upload_image_task
from main_page.permissions import IsSeller


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
            permission_classes = [IsAuthenticated, IsSeller, ChangePriceInOrder]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        order_id = self.kwargs['pk']
        if OrderModel.objects.filter(id=order_id).exists():
            date = OrderModel.objects.get(id=order_id).order_time
            if (datetime.now(timezone.utc) - date) > timedelta(hours=24):
                return OrderOffer.objects.filter(order_id=order_id).all()
        return []

    @swagger_auto_schema(
        operation_description="Вывод всех офферов к заказу.",
        responses={
            200: openapi.Response("Success response", OrderOfferSerializer(many=True)),
            404: openapi.Response("Not found", openapi.Schema(
                type=openapi.TYPE_STRING))
        }
    )
    def list(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        if not OrderModel.objects.filter(id=order_id).exists():
            return Response('Заказ не найден', status=404)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderModelMinifieldViewSet(viewsets.ModelViewSet):
    """Поведение Заказа для отображения в личном кабинете."""

    queryset = OrderModel.objects.all()
    serializer_class = OrderModelMinifieldSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderModel.objects.filter(user_account=user)


@api_view(["POST"])
@check_file_type(["image/jpg", "image/gif", "image/jpeg", "application/pdf"])
@check_user_quota
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.POST.get("order_id")
    image = request.FILES["upload_file"]
    user_id = request.user.id
    name = image.name
    # create new name for image file
    new_name = ServerFileSystem(name, user_id, order_id).generate_new_filename()

    if order_id is None:
        raise errorcode.IncorrectImageOrderUpload()
    if order_id == "" or not order_id.isdigit() or not OrderModel.objects.filter(id=order_id).exists():
        raise errorcode.IncorrectImageOrderUpload()

    # temporary save file
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    with open(f"tmp/{new_name}", "wb+") as file:
        for chunk in image.chunks():
            file.write(chunk)
    temp_file = f"tmp/{new_name}"

    task = celery_upload_image_task.delay(temp_file, user_id, order_id)
    return Response({"task_id": task.id}, status=202)


@api_view(["GET"])
def get_file_order(request, file_id):
    """
    Получение изображения и передача его на фронт
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
