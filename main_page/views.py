import requests
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .error_message import error_responses
from .models import ContactSupport, ContractorAgreement, ContractorData, CooperationOffer
from .permissions import IsContractor
from .serializers import ContactSupportSerializer, ContractorAgreementSerializer, CooperationOfferSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание запроса на сотрудничество",
    responses={
        status.HTTP_400_BAD_REQUEST: error_responses[status.HTTP_400_BAD_REQUEST],
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Получить список запросов на сотрудничество",
    responses={
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление запроса на сотрудничество",
    responses={
        status.HTTP_204_NO_CONTENT: error_responses[status.HTTP_204_NO_CONTENT],
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
class CooperationViewSet(viewsets.ModelViewSet):
    """
    Сохранение обращения аниноминого пользователя на сотрудничество
    """
    queryset = CooperationOffer.objects.all()
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = CooperationOfferSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_description="Получить запрос на сотрудничество",
        responses={
            status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
            status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
        })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание вопроса в поддержку",
    responses={
        status.HTTP_400_BAD_REQUEST: error_responses[status.HTTP_400_BAD_REQUEST],
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Получить список созданных вопросов и ответов",
    responses={
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление конкретного вопроса",
    responses={
        status.HTTP_204_NO_CONTENT: error_responses[status.HTTP_204_NO_CONTENT],
        status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
    }))
class SupportViewSet(viewsets.ModelViewSet):
    """
    Создание вопроса пользователя в поддержку.
    """
    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer
    http_method_names = ["get", "post", "delete"]

    @swagger_auto_schema(
        operation_description="Задать вопрос в поддержку",
        responses={
            status.HTTP_401_UNAUTHORIZED: error_responses[status.HTTP_401_UNAUTHORIZED],
            status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[status.HTTP_500_INTERNAL_SERVER_ERROR]
        })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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


class ContractorAgreementViewSet(viewsets.ModelViewSet):
    queryset = ContractorAgreement.objects.all()
    serializer_class = ContractorAgreementSerializer
    permission_classes = [IsContractor]

    def create(self, request, *args, **kwargs):
        request.data["user_account"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Update ContractorData status
        contractor_data = ContractorData.objects.get(user=request.user)
        contractor_data.is_active = True
        contractor_data.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
