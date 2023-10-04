from utils import errorcode
from utils.decorators import check_file_type, check_user_quota
from utils.errorcode import NotAllowedUser
from utils.storage import CloudStorage

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FileData, OrderModel, OrderOffer
from .permissions import ChangePriceInOrder
from .serializers import OrderOfferSerializer
from .tasks import celery_upload_image_task
from main_page.permissions import IsSeller


class OrderOfferViewSet(viewsets.ModelViewSet):
    """Поведение Оффера"""

    permission_classes = [IsAuthenticated, IsSeller, ChangePriceInOrder]
    queryset = OrderOffer.objects.all()
    serializer_class = OrderOfferSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderOffer.objects.filter(user_account=user)


@api_view(["POST"])
@check_file_type(["image/jpg", "image/jpeg", "application/pdf"])
@check_user_quota
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.POST.get("order_id")
    image = request.FILES["upload_file"]
    user_id = request.user.id
    name = image.name

    if (
        order_id == ""
        or not order_id.isdigit()
        or not OrderModel.objects.filter(id=order_id).exists()
    ):
        raise errorcode.IncorrectImageOrderUpload()

    # temporary save file
    with open(f"tmp/{name}", "wb+") as file:
        for chunk in image.chunks():
            file.write(chunk)
    temp_file = f"tmp/{name}"

    # yandex = CloudStorage()
    # result = yandex.cloud_upload_image(temp_file, user_id, order_id, name)
    #
    # if result['status_code'] == 201:
    #     FileData.objects.create(user_account=request.user, yandex_path=result['yandex_path'])
    #
    #     return Response({"status": "success"})
    # return Response(
    #     {
    #         "status": "failed",
    #         "message": f"Unexpected response from Yandex.Disk: {result['status_code']}",
    #     },
    # )
    task = celery_upload_image_task.delay(temp_file, user_id, order_id)
    return Response({"task_id": task.id}, status=202)


@api_view(["GET"])
def get_file_order(request, file_id):
    """
    Получение изображения и передача его на фронт
    """

    image_data = get_object_or_404(
        FileData, id=file_id
    )  # TODO: Добавить логику ошибки в errorcode.py
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
