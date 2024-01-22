from datetime import datetime, timedelta


from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from app.orders.models import OrderModel, OrderOffer
from .models import Conversation
from .serializers import ChatSerializer


class ChatViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для просмотра списка чатов и создания нового чата."""

    lookup_field = "id"
    http_method_names = ("get", "post", "head", "patch", "delete")
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    ordering = None

    def get_queryset(self):
        """
        Получить все чаты авторизованного пользователя
        с учетом его роли
        """
        user = self.request.user
        if user.is_authenticated:
            if user.role == "contractor":
                offers_ids = OrderOffer.objects.filter(
                    user_account=user,
                ).values_list("pk", flat=True)
                return Conversation.objects.filter(
                    offer__in=offers_ids,
                )
            available_date = datetime.now() - timedelta(
                days=settings.CHATTING["DAYS_TO_UNLOCK"],
            )
            orders_ids = OrderModel.objects.filter(
                user_account=user,
                order_time__lte=available_date,
            ).values_list("pk", flat=True)
            offers_ids = OrderOffer.objects.filter(
                order_id__in=orders_ids,
            ).values_list("pk", flat=True)
            return Conversation.objects.filter(
                client=user,
                is_blocked=False,
                offer__in=offers_ids,
            )
        return None


def room(request):
    return render(request, "chat/room.html")
