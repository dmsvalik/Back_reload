from rest_framework import serializers
from .models import OrderModel, OrderImageModel
from rest_framework.response import Response


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['id', 'user_account', 'card_id', 'order_description', 'order_time', 'state']
        read_only_fields = ['id', ]

    def create(self, validated_data):
        user = self.context['request'].user
        obj = OrderModel.objects.create(**validated_data, user_account=user)
        return obj


class OrderImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderImageModel
        fields = ('id', 'order_id', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6')

    def create(self, validated_data):
        obj = OrderImageModel.objects.create(**validated_data)
        return obj

