from datetime import timedelta

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from django.conf import settings
from django.utils import timezone

from .models import OrderModel, OrderOffer, OrderFileData
from app.questionnaire.serializers import FileSerializer
from app.orders.constants import ORDER_STATE_CHOICES, OfferState, OrderState
from app.utils.errorcode import OrderInWrongStatus


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
            "status": is_selected,
            "order_id__order_time__lt": range_filter,
        }

        queryset = (
            OrderOffer.objects.filter(**query_filter)
            .select_related("user_account")
            .select_related("user_account__contractordata")
        )
        serializer = OfferSerizalizer(
            instance=queryset,
            many=True,
        )
        return serializer.data


class BaseOfferSerizalizer(serializers.ModelSerializer):
    """
    Базовый класс для сериализатора модели Offer
    """

    class Meta:
        model = OrderOffer
        fields = (
            "id",
            "offer_price",
            "offer_execution_time",
            "offer_description",
            "status",
        )


class OfferSerizalizer(BaseOfferSerizalizer):
    contactor_key = serializers.IntegerField(read_only=True)

    class Meta(BaseOfferSerizalizer.Meta):
        fields = BaseOfferSerizalizer.Meta.fields + (
            "user_account",
            "order_id",
            "contactor_key",
        )

    def create(self, validated_data):
        order_obj: OrderModel = validated_data.get("order_id")
        if order_obj.state != OrderState.DRAFT.value:
            raise OrderInWrongStatus()
        return super().create(validated_data)


class OfferOrderSerializer(BaseOfferSerizalizer):
    """
    :contactor_key - номер исполнителч
    :chat_id - ID чата этого оффера
    :files - файлы заказа
    """

    chat_id = serializers.IntegerField(source="chat.pk")
    contactor_name = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta(BaseOfferSerizalizer.Meta):
        fields = BaseOfferSerizalizer.Meta.fields + (
            "contactor_name",
            "chat_id",
            "files",
        )

    def get_contactor_name(self, obj):
        """
        Возвращает название компании исполнителя
        если статус оффера == selected
        Или возвращает номер исполнителя
        как счетчик количества предложений к заказу
        """
        if obj.status == OfferState.SELECTED.value:
            return obj.user_account.contractordata.company_name
        return f"Исполнитель {obj.contactor_key}"

    def get_files(self, obj):
        serializer = FileSerializer(instance=obj.order_id.files, many=True)
        return serializer.data


class OfferContactorSerializer(BaseOfferSerizalizer):
    """
    :order_name - название заказа
    :chat_id - ID чата
    :images - картинки оффера
    :file - файл с тз
    :task - задача заказа
    """

    chat_id = serializers.IntegerField(source="chat.pk")
    order_name = serializers.CharField(source="order_id.name")
    images = serializers.CharField(default=None)
    file = serializers.SerializerMethodField()
    task = serializers.CharField(default=None)

    class Meta(BaseOfferSerizalizer.Meta):
        fields = BaseOfferSerizalizer.Meta.fields + (
            "order_name",
            "chat_id",
            "images",
            "file",
            "task",
        )

    def get_file(self, obj):
        file = (
            OrderFileData.objects.filter(order_id=obj.order_id_id)
            .order_by("date_upload")
            .last()
        )
        serializer = FileSerializer(instance=file, many=False)
        return serializer.data
