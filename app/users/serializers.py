from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserAccount
from .validators import UserValidationFields


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "person_telephone", "surname")


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("id", "email", "name", "person_telephone", "surname", "role")
        validators = [UserValidationFields()]
