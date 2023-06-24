from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import OrderImageModel, OrderOffer
from .serializers import OrderImageSerializer, OrderOfferSerializer


class OrderImageViewSet(viewsets.ModelViewSet):
    """Проверка картинок по продукту + создание картинок с привязкой к продукту"""

    permission_classes = [IsAuthenticated]
    queryset = OrderImageModel.objects.all()
    serializer_class = OrderImageSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderImageModel.objects.filter(order_id__user_account=user)


class OrderOfferViewSet(viewsets.ModelViewSet):
    """Создание Оффера"""

    permission_classes = [IsAuthenticated]
    queryset = OrderOffer.objects.all()
    serializer_class = OrderOfferSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderOffer.objects.filter(user_account=user)
