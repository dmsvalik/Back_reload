from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
        Получить все чаты авторизованного пользователя.
        """
        user = self.request.user
        if user.is_authenticated:
            return user.client_chats.all()
        return None


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
