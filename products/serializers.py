from rest_framework import serializers
from products.models import CategoryModel, ProductModel


class CardModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    card_name = serializers.CharField()


class CategoryModelSeializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name']


class ProductModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['category', 'product_size']

    def create(self, validated_data):
        user = self.context['request'].user
        obj = ProductModel.objects.create(**validated_data, user_account=user, is_ended=False)
        return obj
