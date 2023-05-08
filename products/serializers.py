from rest_framework import serializers
from products.models import CategoryModel


class CardModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    card_name = serializers.CharField()


class CategoryModelSeializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name']