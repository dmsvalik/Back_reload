from rest_framework import serializers

from products.models import (
    CardModel,
    CategoryModel,
    QuestionOptionsModel,
    QuestionsProductsModel,
    ResponseModel,
)


class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = ["id", "name"]


class CategoryModelSeializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["id", "card", "name"]


class QuestionModelSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = QuestionsProductsModel
        exclude = ["category"]

    @staticmethod
    def get_options(obj):
        return QuestionOptionsModel.objects.filter(question=obj).values_list("option", flat=True)


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseModel
        exclude = ["user_account", "order_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        order_id = self.context["request"].order
        return ResponseModel.objects.create(**validated_data, user_account=user, order_id_id=order_id)

