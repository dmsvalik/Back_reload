from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from app.orders.models import OrderModel, OrderOffer
from .models import Conversation
from .serializers import ChatSerializer


class ChatViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет для просмотра списка чатов и создания нового чата."""

    lookup_field = 'id'
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')
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
            if user.role == 'contractor':
                order_ids = OrderOffer.objects.filter(
                    user_account=user,
                ).values_list('order_id', flat=True)
                client_ids = OrderModel.objects.filter(
                    pk__in=order_ids,
                ).values_list('user_account', flat=True)
                queryset = Conversation.objects.filter(
                    contractor=user,
                    is_blocked=False,
                    client__in=client_ids,
                )
                return queryset
            available_date = (datetime.now() - timedelta(
                days=settings.CHATTING['DAYS_TO_UNLOCK'],
            ))
            orders_ids = OrderModel.objects.filter(
                user_account=user,
                order_time__lte=available_date,
            ).values_list(
                'user_account', flat=True
            )
            contractor_ids = OrderOffer.objects.filter(
                pk__in=orders_ids,
            ).values_list('user_account', flat=True)
            queryset = Conversation.objects.filter(
                client=user,
                is_blocked=False,
                contractor__in=contractor_ids,
            )
            return queryset
        return None


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
