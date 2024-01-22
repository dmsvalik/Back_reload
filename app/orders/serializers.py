from datetime import timedelta

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from django.conf import settings
from django.utils import timezone

from .models import OrderModel, OrderOffer, OrderFileData
from app.users.serializers import UserAccountSerializer
from app.questionnaire.serializers import FileSerializer
from app.orders.constants import ORDER_STATE_CHOICES


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
        queryset = [
            file
            for file in OrderFileData.objects.filter(order_id=obj)
            if file.server_path.split(".")[-1] in settings.IMAGE_FILE_FORMATS
        ]
        serializer = FileSerializer(instance=queryset, many=True)
        return serializer.data

    def get_offers(self, obj):
        """
        Получение офферов по ИД заказа
        офферы берутся только
        если заказ был создан
        более hours(24) часов назад
        """
        is_selected = True if obj.state == ORDER_STATE_CHOICES[2][0] else False
        range_filter = timezone.now() - timedelta(
            hours=settings.OFFER_ACCESS_HOURS
        )
        query_filter = {
            "order_id": obj.pk,
            "offer_status": is_selected,
            "order_id__order_time__lt": range_filter,
        }

        queryset = (
            OrderOffer.objects.filter(**query_filter)
            .select_related("user_account")
            .select_related("user_account__contractordata")
        )
        serializer = OfferHalfSerializer(
            instance=queryset,
            many=True,
        )
        return serializer.data


class OfferIDSerizalizer(serializers.ModelSerializer):
    """
    Базовый класс для сериализатора модели Offer
    """

    class Meta:
        model = OrderOffer
        fields = ("id",)


class OfferHalfSerializer(OfferIDSerizalizer):
    """
    Сериализатор для вывода полей
    :id - ID оффера
    :contactor_key - номер исполнителч
    :chat_id: ID чата этого оффера
    """

    chat_id = serializers.IntegerField(source="chat.pk")
    contactor_name = serializers.SerializerMethodField()

    class Meta(OfferIDSerizalizer.Meta):
        fields = OfferIDSerizalizer.Meta.fields + ("contactor_name", "chat_id")

    def get_contactor_name(self, obj):
        if obj.offer_status:
            return obj.user_account.contractordata.company_name
        return f"Исполнитель {obj.contactor_key}"


class OfferSerializer(OfferIDSerizalizer):
    class Meta(OfferIDSerizalizer.Meta):
        fields = OfferIDSerizalizer.Meta.fields + (
            "id",
            "offer_price",
            "offer_execution_time",
            "offer_description",
            "contactor_key",
        )


class OrderOfferSerializer(OfferSerializer):
    user_account = UserAccountSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    order_id = serializers.SerializerMethodField(read_only=True)

    class Meta(OfferSerializer.Meta):
        fields = OfferSerializer.Meta.fields + (
            "user_account",
            "order_id",
        )
        read_only_fields = (
            "id",
            "user_account",
            "order_id",
        )

    def get_order_id(self, value):
        return self.context["view"].kwargs["pk"]

    # def validate(self, data):
    #     order_id = self.context["view"].kwargs["pk"]
    #     if not OrderModel.objects.filter(id=order_id).exists():
    #         raise errorcode.OrderIdNotFound()
    #     user = self.context["view"].request.user
    #     if user.role != "contractor":
    #         raise errorcode.NotContractorOffer()
    #     # Вот тут надо продумать как автоматически создавать ContractorData
    #     # если у пользователя role = 'contractor'
    #     if OrderModel.objects.get(id=order_id).state != "offer":
    #         raise errorcode.OrderInWrongStatus()
    #     if not ContractorData.objects.get(user=user).is_active:
    #         raise errorcode.ContractorIsInactive()
    #     if OrderOffer.objects.filter(
    #         user_account=user, order_id=order_id
    #     ).exists():
    #         raise errorcode.UniqueOrderOffer()

    #     return data
