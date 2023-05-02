from rest_framework import serializers
from .models import PersonalClientData

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')

class PersonalClientSerializer(serializers.Serializer):
    person_telephone = serializers.CharField()
    person_name = serializers.CharField()
    person_address = serializers.CharField()

    def create(self, validated_data):
        return PersonalClientData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.person_telephone = validated_data.get('person_telephone', instance.person_telephone)
        instance.person_name = validated_data.get('person_name', instance.person_name)
        instance.person_address = validated_data.get('person_address', instance.person_address)
        instance.save()
        return instance

