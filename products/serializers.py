from rest_framework import serializers


class CardModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    card_name = serializers.CharField()