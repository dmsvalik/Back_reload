from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from utils import errorcode
from main_page.permissions import IsSeller
from .models import OrderImageModel, OrderOffer
from .permissions import ChangePriceInOrder
from .serializers import OrderImageSerializer, OrderOfferSerializer
from utils.decorators import check_file_type, check_user_quota




class OrderImageViewSet(viewsets.ModelViewSet):
    """Проверка картинок по продукту + создание картинок с привязкой к продукту - test """

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

@check_user_quota
@api_view(['POST'])
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.POST.get('order_id')
    if 'image' not in request.FILES:
        return Response({'error': 'Ключ "image" отсутствует в загруженных файлах'}, status=400)
    image = request.FILES["image"]
    print(image)
    if order_id == '' or not order_id.isdigit():
        raise errorcode.IncorrectImageOrderUpload()

    return Response({'status': 'success'})
