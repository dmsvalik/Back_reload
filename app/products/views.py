from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from .models import Category
from .serializers import CategorySerializer, QuestionnaireShortTypeSerializer
from .swagger_documentation import products as swagger
from app.questionnaire.models import QuestionnaireType


@method_decorator(
    name="list", decorator=swagger_auto_schema(**swagger.CategoryList.__dict__)
)
class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    """Вьюсет категорий. Получение списка категорий"""

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @swagger_auto_schema(**swagger.QuestionnaireTypeGetList.__dict__)
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
