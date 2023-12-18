from django.contrib.sites.shortcuts import get_current_site
from djoser.views import UserViewSet
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings as djoser_settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings

from app.sending.signals import new_notification
from app.sending.views import send_user_notifications
from app.users.tasks import send_django_users_emails
from app.utils.views import recalculate_quota
from app.users.utils import calculate_order_files_size_by_cookie_key
from config import settings


# class ActivateUser(UserViewSet):
#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         kwargs.setdefault("context", self.get_serializer_context())
#
#         # this line is the only change from the base implementation.
#         kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}
#         return serializer_class(*args, **kwargs)
#
#     @method_decorator(name='list', decorator=swagger_auto_schema(
#         operation_description="Получить список запросов на сотрудничество",
#         responses={
#             status.HTTP_400_BAD_REQUEST: error_responses[status.HTTP_400_BAD_REQUEST],
#             status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
#         }
#     ))
#     def activation(self, request, uid, token, *args, **kwargs):
#         super().activation(request, *args, **kwargs)
#         return Response({"активация": "активация аккаунта прошла успешно"})
#
#
# def reset_password(request, uid, token):
#     """ Тестовый сброс пароля - заменить на сторону фронта """
#
#     if request.method == "POST":
#         # проверки на стороне фронта на корректность пароля - не пустое поле и тд
#         new_pass = request.POST["new_pass"]
#         uid_new = request.POST["uid_data"]
#         token_new = request.POST["token_data"]
#
#         # надо поменять url когда на сервере будет
#         url = "http://127.0.0.1:8000/auth/users/reset_password_confirm/"
#         data = {"uid": uid_new, "token": token_new, "new_password": new_pass}
#         headers = {"Accept": "application/json"}
#
#         # отправляем POST запрос и меняем пароль
#         requests.post(url, headers=headers, data=data)
#
#         return JsonResponse({"обновление пароля": "22 прошло успешно"})
#
#     return render(
#         request, "main_page/reset_password.html", {"uid": uid, "token_uid": token}
#     )


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
        key = request.COOKIES.get('key')
        user = self.user_instance

        if key:
            sizes: tuple[int] | None = calculate_order_files_size_by_cookie_key(user, key)
            if sizes: recalculate_quota(user, *sizes)
            response.delete_cookie('key')

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
            context = {"order_name": order.name,
                       "username": user.name}
            if user.notifications:
                send_user_notifications(user, "ORDER_CREATE_CONFIRMATION", context, [get_user_email(user)])
        except Exception:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


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
        key = request.COOKIES.get('key')
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if key:
            sizes: tuple[int] | None = calculate_order_files_size_by_cookie_key(user, key)
            if sizes: recalculate_quota(user, *sizes)
            response.delete_cookie('key')

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
