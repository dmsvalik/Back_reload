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
from django.utils.decorators import method_decorator


from app.sending.serializers import DisableNotificationsSerializer
from app.users.tasks import send_django_users_emails
from app.users import signals
from app.orders.models import OrderModel
from config.settings import DJOSER_EMAIL_CLASSES, ORDER_COOKIE_KEY_NAME

from .swagger_documentation import users as swagger
from .utils.helpers import site_data_from_request


@method_decorator(
    name="set_username",
    decorator=swagger_auto_schema(**swagger.SetUsernameDocs.__dict__),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(**swagger.UsersListDocs.__dict__),
)
@method_decorator(
    name="resend_activation",
    decorator=swagger_auto_schema(**swagger.ResendActivationDocs.__dict__),
)
@method_decorator(
    name="reset_password",
    decorator=swagger_auto_schema(**swagger.ResetPasswordDocs.__dict__),
)
@method_decorator(
    name="set_password",
    decorator=swagger_auto_schema(**swagger.SetPasswordDocs.__dict__),
)
@method_decorator(
    name="reset_password_confirm",
    decorator=swagger_auto_schema(**swagger.ResetPasswordConfirmDocs.__dict__),
)
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
                DJOSER_EMAIL_CLASSES["ACTIVATION"],
                context,
                user.id,
                [
                    user.email,
                ],
            )
        elif djoser_settings.SEND_CONFIRMATION_EMAIL:
            send_django_users_emails.delay(
                DJOSER_EMAIL_CLASSES["CONFIRMATION"],
                context,
                user.id,
                [
                    user.email,
                ],
            )

    @swagger_auto_schema(**swagger.UsersCreateDocs.__dict__)
    def create(self, request, *args, **kwargs):
        """
        Формирование ответа
        Проверка на наличие ключа заказа в куки
        Пересчет, выделенного для файлов, размера диска пользователя
        при наличии ключа в куки
        """
        response = super().create(request, *args, **kwargs)
        cookie_key = request.COOKIES.get(ORDER_COOKIE_KEY_NAME)

        if cookie_key:
            order: OrderModel = OrderModel.objects.filter(
                key=cookie_key, user_account__isnull=True
            ).first()
            if order:
                order.user_account = self.user_instance
                order.save()
            signals.quota_recalculate.send(
                sender=self.__class__, user=self.user_instance, order=order
            )
            response.delete_cookie(ORDER_COOKIE_KEY_NAME)

        return response

    @swagger_auto_schema(**swagger.UserActivationDocs.__dict__)
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
                DJOSER_EMAIL_CLASSES["CONFIRMATION"],
                context,
                user.id,
                [
                    user.email,
                ],
            )

        order = user.ordermodel_set.filter(state="draft").first()
        if order:
            order.state = "offer"
            order.save()
            signals.send_notify.send(
                sender=self.__class__, user=user, order=order
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger.DisableNotificationsDocs.__dict__)
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

    @swagger_auto_schema(**swagger.UserMeReadDocs.__dict__)
    @swagger_auto_schema(**swagger.UserMeUpdateDocs.__dict__)
    @swagger_auto_schema(**swagger.UserMePartialUpdateDocs.__dict__)
    @swagger_auto_schema(**swagger.UserMeDeleteDocs.__dict__)
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)


class CustomTokenViewBase(TokenViewBase):
    @swagger_auto_schema(**swagger.TokenJWTCreateDocs.__dict__)
    def post(self, request, *args, **kwargs):
        """
        Создание токена
        Проверка на наличие ключа заказа в куки
        Пересчет, выделенного для файлов, размера диска пользователя и
        отправка уведомления об активации заказа при наличии ключа в куки.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        cookie_key = request.COOKIES.get(ORDER_COOKIE_KEY_NAME)
        response = Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )

        if cookie_key:
            order: OrderModel = OrderModel.objects.filter(
                key=cookie_key, user_account__isnull=True
            ).first()
            if order:
                order.user_account = user
                order.save()
            signals.quota_recalculate.send(
                sender=self.__class__,
                user=user,
                order=order,
                change_order_state=True,
            )
            signals.send_notify.send(
                sender=self.__class__, user=user, order=order
            )
            response.delete_cookie(ORDER_COOKIE_KEY_NAME)

        return response


class CustomTokenObtainPairView(CustomTokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER
