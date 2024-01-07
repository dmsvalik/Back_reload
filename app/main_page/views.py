from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .error_message import error_responses
from .models import (
    ContactSupport,
    ContractorAgreement,
    ContractorData,
    CooperationOffer,
)
from .permissions import IsContractor
from .serializers import (
    ContactSupportSerializer,
    ContractorAgreementSerializer,
    CooperationOfferSerializer,
)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание запроса на сотрудничество",
        responses={
            status.HTTP_400_BAD_REQUEST: error_responses[
                status.HTTP_400_BAD_REQUEST
            ],
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получить список запросов на сотрудничество",
        responses={
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление запроса на сотрудничество",
        responses={
            status.HTTP_204_NO_CONTENT: error_responses[
                status.HTTP_204_NO_CONTENT
            ],
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_404_NOT_FOUND: error_responses[
                status.HTTP_404_NOT_FOUND
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
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
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_404_NOT_FOUND: error_responses[
                status.HTTP_404_NOT_FOUND
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание вопроса в поддержку",
        responses={
            status.HTTP_400_BAD_REQUEST: error_responses[
                status.HTTP_400_BAD_REQUEST
            ],
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получить список созданных вопросов и ответов",
        responses={
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление конкретного вопроса",
        responses={
            status.HTTP_204_NO_CONTENT: error_responses[
                status.HTTP_204_NO_CONTENT
            ],
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_404_NOT_FOUND: error_responses[
                status.HTTP_404_NOT_FOUND
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
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
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_404_NOT_FOUND: error_responses[
                status.HTTP_404_NOT_FOUND
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание соглашения с исполнителем.",
        responses={
            status.HTTP_400_BAD_REQUEST: error_responses[
                status.HTTP_400_BAD_REQUEST
            ],
            status.HTTP_401_UNAUTHORIZED: error_responses[
                status.HTTP_401_UNAUTHORIZED
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ],
        },
    ),
)
class ContractorAgreementViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания соглашения с исполнителем."""

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
