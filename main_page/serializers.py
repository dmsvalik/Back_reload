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
    user_account_id = serializers.IntegerField()
    person_telephone = serializers.CharField()
    person_name = serializers.CharField()
    person_address = serializers.CharField()

