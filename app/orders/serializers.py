from datetime import timedelta, datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .models import OrderModel, OrderOffer, OrderFileData
from app.main_page.models import ContractorData
from app.users.serializers import UserAccountSerializer
from app.questionnaire.serializers import FileSerializer
from app.utils import errorcode


User = get_user_model()


class OrderModelSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""

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


class AllOrdersClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода краткой информации по всем заказам пользователя.
    """

    contractor = SerializerMethodField()
    worksheet = serializers.Field(default=None)
    images = SerializerMethodField()
    offers = SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "name",
            "order_time",
            "state",
            "contractor",
            "worksheet",
            "images",
            "offers",
        ]
        read_only_fields = [
            "id",
        ]

    def get_contractor(self, obj):
        """Метод для подсчета оферов на конкретный заказ."""
        return OrderOffer.objects.filter(order_id=obj.id).count()

    def get_images(self, obj):
        queryset = OrderFileData.objects.filter(order_id=obj)
        serializer = FileSerializer(instance=queryset, many=True)
        return serializer.data

    def get_offers(self, obj):
        """
        Получение офферов по ИД заказа
        и текущему пользователю
        только офферы берутся только
        если заказ был создан
        более hours(24) часов назад
        """
        current_user = self._get_current_user()
        hours = timedelta(hours=24)
        today = datetime.now()
        range_filter = today - hours

        queryset = OrderOffer.objects.filter(
            order_id=obj,
            user_account=current_user,
            order_id__order_time__lt=range_filter,
        ).values("id")
        serializer = OfferSerializer(
            instance=queryset,
            many=True,
        )
        return serializer.data

    def _get_current_user(self) -> User:
        request: HttpRequest = self.context["request"]
        return request.user


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOffer
        fields = [
            "id",
            "offer_price",
            "offer_execution_time",
            "offer_description",
        ]


class OrderOfferSerializer(OfferSerializer):
    user_account = UserAccountSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    order_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderOffer
        read_only_fields = (
            "id",
            "user_account",
            "order_id",
        )

    def get_order_id(self, value):
        return self.context["view"].kwargs["pk"]

    def validate(self, data):
        order_id = self.context["view"].kwargs["pk"]
        if not OrderModel.objects.filter(id=order_id).exists():
            raise errorcode.OrderIdNotFound()
        user = self.context["view"].request.user
        if user.role != "contractor":
            raise errorcode.NotContractorOffer()
        # Вот тут надо продумать как автоматически создавать ContractorData
        # если у пользователя role = 'contractor'
        if OrderModel.objects.get(id=order_id).state != "offer":
            raise errorcode.OrderInWrongStatus()
        if not ContractorData.objects.get(user=user).is_active:
            raise errorcode.ContractorIsInactive()
        if OrderOffer.objects.filter(
            user_account=user, order_id=order_id
        ).exists():
            raise errorcode.UniqueOrderOffer()

        return data
