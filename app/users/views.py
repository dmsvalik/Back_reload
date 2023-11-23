import requests
from django.http.response import JsonResponse
from django.shortcuts import render
from djoser.views import UserViewSet
from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings

from app.main_page.error_message import error_responses
from app.orders.models import OrderModel


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}
        return serializer_class(*args, **kwargs)

    @method_decorator(name='list', decorator=swagger_auto_schema(
        operation_description="Получить список запросов на сотрудничество",
        responses={
            status.HTTP_400_BAD_REQUEST: error_responses[status.HTTP_400_BAD_REQUEST],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
        }
    ))
    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response({"активация": "активация аккаунта прошла успешно"})


def reset_password(request, uid, token):
    """ Тестовый сброс пароля - заменить на сторону фронта """

    if request.method == "POST":
        # проверки на стороне фронта на корректность пароля - не пустое поле и тд
        new_pass = request.POST["new_pass"]
        uid_new = request.POST["uid_data"]
        token_new = request.POST["token_data"]

        # надо поменять url когда на сервере будет
        url = "http://127.0.0.1:8000/auth/users/reset_password_confirm/"
        data = {"uid": uid_new, "token": token_new, "new_password": new_pass}
        headers = {"Accept": "application/json"}

        # отправляем POST запрос и меняем пароль
        requests.post(url, headers=headers, data=data)

        return JsonResponse({"обновление пароля": "22 прошло успешно"})

    return render(
        request, "main_page/reset_password.html", {"uid": uid, "token_uid": token}
    )


class CustomUserViewSet(UserViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        headers = self.get_success_headers(serializer.data)
        key = request.COOKIES.get('key')
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        if key:
            try:
                order = OrderModel.objects.get(key=key, user_account__isnull=True)
            except OrderModel.DoesNotExist:
                order = None
            if order:
                order.user_account = user
                order.save()
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

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)
        orders = user.ordermodel_set.all()
        for order in orders:
            order.state = "offer"
            order.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenViewBase(TokenViewBase):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = serializer.user
        key = request.COOKIES.get('key')
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        if key:
            try:
                order = OrderModel.objects.get(key=key, user_account__isnull=True)
            except OrderModel.DoesNotExist:
                order = None
            if order:
                order.user_account = user
                order.state = "offer"
                order.save()
            response.delete_cookie('key')
        return response


class CustomTokenObtainPairView(CustomTokenViewBase):

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER
