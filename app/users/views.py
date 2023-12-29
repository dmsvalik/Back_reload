from djoser.views import UserViewSet
from djoser import signals as djoser_signals
from djoser.conf import settings as djoser_settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings


from app.sending.serializers import DisableNotificationsSerializer
from app.sending.signals import new_notification
from app.users.tasks import send_django_users_emails
from app.users import signals
from app.orders.models import OrderModel
from config.settings import DJOSER

from .utils.helpers import site_data_from_request


class CustomUserViewSet(UserViewSet):
    def perform_create(self, serializer, *args, **kwargs):
        """
        Сохранение пользователя после регистрации и отправка сообщения на почту
        """
        user = serializer.save(*args, **kwargs)
        self.user_instance = user

        djoser_signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = site_data_from_request(self.request)
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            send_django_users_emails.delay(
                DJOSER.get("EMAIL").get("activation"),
                context,
                user.id,
                [
                    user.email,
                ],
            )
            new_notification.send(
                sender=self.__class__,
                user=user,
                theme="Письмо активации аккаунта",
                type="email",
            )
        elif djoser_settings.SEND_CONFIRMATION_EMAIL:
            send_django_users_emails.delay(
                DJOSER.get("EMAIL").get("confirmation"),
                context,
                user.id,
                [
                    user.email,
                ],
            )
            new_notification.send(
                sender=self.__class__,
                user=user,
                theme="Подтверждение активации аккаунта",
                type="email",
            )

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
            order: OrderModel = OrderModel.objects.filter(
                key=cookie_key, user_account__isnull=True
            ).first()
            signals.quota_recalculate.send(
                sender=self.__class__, user=self.user_instance, order=order
            )
            response.delete_cookie("key")

        return response

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        """
        Активация аккаунта
        Проверка на наличие ключа заказа в куки
        Активация заказа при наличии у пользователя заказа в статусе draft.
        Отправка уведомления об активации заказа
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        djoser_signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if djoser_settings.SEND_CONFIRMATION_EMAIL:
            context = site_data_from_request(request)
            send_django_users_emails.delay(
                DJOSER.get("EMAIL").get("confirmation"),
                context,
                user.id,
                [
                    user.email,
                ],
            )
            new_notification.send(
                sender=self.__class__,
                user=user,
                theme="Подтверждение активации аккаунта",
                type="email",
            )

        order = user.ordermodel_set.filter(state="draft").first()
        if order:
            order.state = "offer"
            order.save()
            signals.send_notify.send(
                sender=self.__class__, user=user, order=order
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=DisableNotificationsSerializer(), method="POST"
    )
    @action(["post"], detail=False, permission_classes=[AllowAny])
    def disable_notifications(self, request, *args, **kwargs):
        """
        Отключение всех типов уведомлений пользователя.
        """
        context = self.get_serializer_context()
        serializer = DisableNotificationsSerializer(
            data=request.data, context=context
        )
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
        Пересчет, выделеного для файлов, размера диска пользователя и
        отправка уведомления об активации заказа при наличии ключа в куки.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        cookie_key = request.COOKIES.get("key")
        response = Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )

        if cookie_key:
            order: OrderModel = OrderModel.objects.filter(
                key=cookie_key, user_account__isnull=True
            ).first()
            signals.quota_recalculate.send(
                sender=self.__class__,
                user=user,
                order=order,
                change_order_state=True,
            )
            signals.send_notify.send(
                sender=self.__class__, user=user, order=order
            )
            response.delete_cookie("key")

        return response


class CustomTokenObtainPairView(CustomTokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER
