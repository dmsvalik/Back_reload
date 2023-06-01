from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from config import settings
from chat.serializers import MessageModelSerializer, UserModelSerializer
from chat.models import MessageModel
from main_page.models import UserAccount

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):

        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))

        # тут когда кликаем на фронте js на пользователя появляется переписка то есть target - тот на кого кликаем
        target = self.request.query_params.get('target', None)

        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__name=target) |
                Q(recipient__name=target, user=request.user))

        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)

        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = UserAccount.objects.all()

    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)


#
# class UserModelViewSet(ModelViewSet):
#
#     queryset = User.objects.all()
#
#     serializer_class = UserModelSerializer
#     allowed_methods = ('GET', 'HEAD', 'OPTIONS')
#     pagination_class = None  # Get all user
#
#     def list(self, request, *args, **kwargs):
#         # проверяем, кто сделал оффер именно этому пользователю. выходим на него через id
#         check_offer_user = OfferModel.objects.filter(order_id__user=request.user.id)
#         # готовим список id магазинов с предложениями (в будущем тут можно добавить логику по фильтрации тех оферов
#         # которые принял пользователь
#         list_users = [item.user_shop.id for item in check_offer_user]
#
#         # теперь проверяем если вам кто-то написал сообщение(например если вы магазин и вам написал юзер)
#         check_message_user = MessageModel.objects.filter(recipient=request.user.id)
#         # готовим список id юзеров, которые написали магазину и прибавляем к списку выше
#         list_users += [item.user.id for item in check_message_user]
#
#         # теперь передаем всех пользователей с которым идут переписки для вывода юзеров на фронте
#         self.queryset = self.queryset.filter(id__in=list_users).exclude(id=request.user.id)
#
#         return super(UserModelViewSet, self).list(request, *args, **kwargs)
#
