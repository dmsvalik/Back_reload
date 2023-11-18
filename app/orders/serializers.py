from app.utils import errorcode

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import FileData, OrderModel, OrderOffer
from app.main_page.models import ContractorData
from app.main_page.serializers import UserAccountSerializer


class FilePreviewSerializer(serializers.ModelSerializer):
    preview_path = SerializerMethodField()

    class Meta:
        model = FileData
        fields = [
            "id",
            "preview_path",
        ]
        read_only_fields = [
            "id",
            "preview_path",
        ]

    def get_preview_path(self, obj):
        server_path = obj.server_path
        return '/documents/' + server_path.split('files/')[-1]


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


class AllOrdersClientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода краткой информации по всем заказам пользователя."""

    contractor = SerializerMethodField()
    files = SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "name",
            "order_time",
            "state",
            "contractor",
            "files",
        ]
        read_only_fields = [
            "id",
        ]

    def get_contractor(self, obj):
        """Метод для подсчета оферов на конкретный заказ."""
        return OrderOffer.objects.filter(order_id=obj.id).count()

    def get_files(self, obj):
        queryset = FileData.objects.filter(order_id=obj.id)
        serializer = FilePreviewSerializer(queryset, many=True, )
        return serializer.data


class OrderOfferSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True, default=serializers.CurrentUserDefault())
    order_id = serializers.SerializerMethodField(read_only=True)

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
        read_only_fields = (
            "id",
            "user_account",
            "order_id",
        )

    def get_order_id(self, value):
        return self.context['view'].kwargs['pk']

    def validate(self, data):
        order_id = self.context['view'].kwargs['pk']
        if not OrderModel.objects.filter(id=order_id).exists():
            raise errorcode.OrderIdNotFound()
        user = self.context['view'].request.user
        if user.role != 'contractor':
            raise errorcode.NotContractorOffer()
        # Вот тут надо продумать как автоматически создавать ContractorData
        # если у пользователя role = 'contractor'
        if OrderModel.objects.get(id=order_id).state != "offer":
            raise errorcode.OrderInWrongStatus()
        if not ContractorData.objects.get(user=user).is_active:
            raise errorcode.ContractorIsInactive()
        if OrderOffer.objects.filter(user_account=user, order_id=order_id).exists():
            raise errorcode.UniqueOrderOffer()

        return data

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     contractor_data = ContractorData.objects.get(user=user)
    #     # try:
    #     #     contractor_data = ContractorData.objects.get(user_account_id=user)
    #     # except TypeError:
    #     #     raise serializers.ValidationError("Вы не являетесь продавцом")
    #     """проверяем если продавец активен, не заблокирован"""
    #     if not contractor_data.is_active:
    #         raise serializers.ValidationError("Вы не можете сделать оффер")
    #     # """ставим заглушку на цену, тк ее можно указать только через 24 часа после оффера"""
    #     # validated_data["offer_price"] = " "
    #     validated_data.pop(
    #         "user_account", None
    #     )  # Ensure 'user_account' is not in validated_data
    #     return OrderOffer.objects.create(**validated_data, user_account=user)
