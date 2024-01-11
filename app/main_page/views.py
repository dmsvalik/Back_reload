from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

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
from .swagger_documentation import main_page as swagger


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(**swagger.CooperationCreate.__dict__),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(**swagger.CooperationList.__dict__),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(**swagger.CooperationDelete.__dict__),
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

    @swagger_auto_schema(**swagger.CooperationDetail.__dict__)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(**swagger.SupportCreate.__dict__),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(**swagger.SupportList.__dict__),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(**swagger.SupportDelete.__dict__),
)
class SupportViewSet(viewsets.ModelViewSet):
    """
    Создание вопроса пользователя в поддержку.
    """

    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer
    http_method_names = ["get", "post", "delete"]

    @swagger_auto_schema(**swagger.SupportRetrieve.__dict__)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        **swagger.ContractorAgreementCreate.__dict__
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
