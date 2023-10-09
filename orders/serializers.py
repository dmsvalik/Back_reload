from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import OrderModel, OrderOffer
from main_page.models import SellerData


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = [
            "id",
            "user_account",
            "order_description",
            "order_time",
            "state",
        ]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return OrderModel.objects.create(**validated_data, user_account=user)


class OrderModelMinifieldSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода краткой информации по всем заказам пользователя."""

    contractor = SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "order_description",
            "order_time",
            "state",
            "contractor",
        ]
        read_only_fields = [
            "id",
        ]

    def get_contractor(self, obj):
        """Метод для подсчета оферов на конкретный заказ."""
        return OrderOffer.objects.filter(order_id=obj.id).count()


class OrderOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOffer
        fields = [
            "id",
            "user_account",
            "order_id",
            "offer_price",
            "offer_execution_time",
            "offer_description",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        seller_data = SellerData.objects.get(user=user)
        # try:
        #     seller_data = SellerData.objects.get(user_account_id=user)
        # except TypeError:
        #     raise serializers.ValidationError("Вы не являетесь продавцом")
        """проверяем если продавец активен, не заблокирован"""
        if not seller_data.is_activ:
            raise serializers.ValidationError("Вы не можете сделать оффер")
        # """ставим заглушку на цену, тк ее можно указать только через 24 часа после оффера"""
        # validated_data["offer_price"] = " "
        validated_data.pop(
            "user_account", None
        )  # Ensure 'user_account' is not in validated_data
        return OrderOffer.objects.create(**validated_data, user_account=user)
