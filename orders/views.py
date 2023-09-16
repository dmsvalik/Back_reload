from utils import errorcode
from utils.decorators import check_user_quota, check_file_type
from utils.storage import CloudStorage

from django.core.files.temp import NamedTemporaryFile
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OrderImageModel, OrderOffer
from .permissions import ChangePriceInOrder
from .serializers import OrderImageSerializer, OrderOfferSerializer
from main_page.permissions import IsSeller


class OrderImageViewSet(viewsets.ModelViewSet):
    """Проверка картинок по продукту + создание картинок с привязкой к продукту - test"""

    permission_classes = [IsAuthenticated]
    queryset = OrderImageModel.objects.all()
    serializer_class = OrderImageSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderImageModel.objects.filter(order_id__user_account=user)


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
@check_file_type(["jpg",])
@check_user_quota
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.POST.get("order_id")
    image = request.FILES["upload_file"]
    user_id = request.user.id
    name = image.name

    if order_id == "" or not order_id.isdigit():
        raise errorcode.IncorrectImageOrderUpload()

    # save temp version of the file in system, for celery task
    temp_file = NamedTemporaryFile(delete=True)
    for block in image.chunks():
        temp_file.write(block)
    temp_file.flush()

    yandex = CloudStorage()
    response_code = yandex.cloud_upload_image(temp_file.name, user_id, order_id, name)
    temp_file.close()

    if response_code == 201:
        return Response({"status": "success"})
    return Response(
        {
            "status": "failed",
            "message": f"Unexpected response from Yandex.Disk: {response_code}",
        },
    )
