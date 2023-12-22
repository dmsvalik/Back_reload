from django.contrib.sites.shortcuts import get_current_site
from djoser.views import UserViewSet
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings as djoser_settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings


from app.sending.serializers import DisableNotificationsSerializer
from app.sending.signals import new_notification
from app.sending.views import send_user_notifications
from app.users.tasks import send_django_users_emails
from app.users import signals
from app.orders.models import OrderModel
from config import settings


class CustomUserViewSet(UserViewSet):

    def perform_create(self, serializer, *args, **kwargs):
        """
        Сохранение пользователя после регистрации и отправка сообщения на почту
        """
        user = serializer.save(*args, **kwargs)
        self.user_instance = user

        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        # context = {"user": user}
        context = site_data_from_request(self.request)
        to = [get_user_email(user)]
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            # djoser_settings.EMAIL.activation(self.request, context).send(to)
            send_django_users_emails.delay(
                "EMAIL.activation",
                context,
                user.id,
                to)
            new_notification.send(sender=self.__class__, user=user, theme="Письмо активации аккаунта",
                                  type="email")
        elif djoser_settings.SEND_CONFIRMATION_EMAIL:
            # djoser_settings.EMAIL.confirmation(self.request, context).send(to)
            send_django_users_emails.delay(
                "EMAIL.confirmation",
                context,
                user.id,
                to)
            new_notification.send(sender=self.__class__, user=user, theme="Подтверждение активации аккаунта",
                                  type="email")

    def create(self, request, *args, **kwargs):
        """
        Формирование ответа
        Проверка на наличие ключа заказа в куки
        Пересчет, выделеного для файлов, размера диска пользователя
        при наличии ключа в куки
        """
        response = super().create(request, *args, **kwargs)
        cookie_key = request.COOKIES.get("key")

        if cookie_key:
            order: OrderModel = OrderModel.objects.filter(key=cookie_key, user_account__isnull=True).first()
            signals.quota_recalculate.send(
                sender=self.__class__,
                user=self.user_instance,
                order=order
                )
            response.delete_cookie("key")

        return response

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if djoser_settings.SEND_CONFIRMATION_EMAIL:
            # context = {"user": user}
            to = [get_user_email(user)]
            # djoser_settings.EMAIL.confirmation(self.request, context).send(to)
            context = site_data_from_request(request)
            send_django_users_emails.delay(
                "EMAIL.confirmation",
                context,
                user.id,
                to)
            new_notification.send(sender=self.__class__, user=user, theme="Подтверждение активации аккаунта",
                                  type="email")
        try:
            order = user.ordermodel_set.get(state="draft")
            order.state = "offer"
            order.save()
            context = {"order_id": order.id,
                       "user_id": user.id}
            if user.notifications:
                send_user_notifications(user, "ORDER_CREATE_CONFIRMATION", context, [get_user_email(user)])
        except Exception:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=DisableNotificationsSerializer(),
        method="POST"
    )
    @action(["post"], detail=False, permission_classes=[AllowAny])
    def disable_notifications(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = DisableNotificationsSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.notifications = False
        user.save()
        user.usernotifications_set.all().delete()
        return Response(status=204)



class CustomTokenViewBase(TokenViewBase):
    def post(self, request, *args, **kwargs):
        """
        Создание токена
        Проверка на наличие ключа заказа в куки
        Пересчет, выделеного для файлов, размера диска пользователя
        при наличии ключа в куки
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        cookie_key = request.COOKIES.get("key")
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if cookie_key:
            order: OrderModel = OrderModel.objects.filter(key=cookie_key, user_account__isnull=True).first()
            signals.quota_recalculate.send(
                sender=self.__class__,
                user=user,
                order=order,
                change_order_state=True
                )
            signals.send_notify.send(
                sender=self.__class__,
                user=user,
                order=order
            )
            response.delete_cookie("key")

        return response


class CustomTokenObtainPairView(CustomTokenViewBase):

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


def site_data_from_request(request):
    context = {}
    site = get_current_site(request)
    domain = getattr(settings, 'DOMAIN', '') or site.domain
    protocol = 'https' if request.is_secure() else 'http'
    site_name = getattr(settings, 'SITE_NAME', '') or site.name
    context.update({
        'domain': domain,
        'protocol': protocol,
        'site_name': site_name,
    })
    return context
