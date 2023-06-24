from rest_framework import serializers

from products.models import (
    CardModel,
    CategoryModel,
    QuestionOptionsModel,
    QuestionsProductsModel,
    ResponseModel,
)
from orders.models import OrderModel


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
        return ResponseModel.objects.create(**validated_data, user_account=user)


    # проблема - это цикл, код запускается столько раз, сколько объектов в списке и если мы сюда поставим создание
    # заказа, то к каждому объекту будет создан отдельный заказ. Поэтому мы просто передадим на фронт id всех созданных
    # ответов и в дальнейшем шаге мы создадим заказ с этими id

    # order_create = OrderModel.objects.create(
    #     user_account=user,
    #     state="creating",
    # )
    #
    # order_instance = OrderModel.objects.get(id=order_create.id)