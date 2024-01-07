from rest_framework import serializers

from app.products.models import Category
from app.questionnaire.models import QuestionnaireType


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ["id", "name", "active"]


class QuestionnaireShortTypeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода краткой информации о типах анкет."""

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "active"]
