from rest_framework import serializers

from products.models import CardModel


class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = ["id", "name"]
