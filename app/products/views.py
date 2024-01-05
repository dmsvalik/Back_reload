from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Category
from .serializers import CategorySerializer, QuestionnaireShortTypeSerializer
from .swagger_documentation.products import QuestionnaireTypeGetList
from app.questionnaire.models import QuestionnaireType


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    """Вьюсет категорий. Получение списка категорий"""

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @swagger_auto_schema(
        operation_description=QuestionnaireTypeGetList.operation_description,
        request_body=QuestionnaireTypeGetList.request_body,
        responses=QuestionnaireTypeGetList.responses,
        method="GET",
    )
    @action(
        detail=True,
        methods=[
            "get",
        ],
    )
    def questionnaires(self, request, pk):
        """Получение списка типов анкет к определенной категории."""
        queryset = QuestionnaireType.objects.filter(category=pk)
        serializer = QuestionnaireShortTypeSerializer(queryset, many=True)
        return Response(serializer.data)
