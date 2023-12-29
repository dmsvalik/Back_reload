from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import UserValidationFields


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "person_telephone",
            "surname",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserAccountSerializer(serializers.ModelSerializer):
    """Сериализатор вывода и обновления данных о пользователе."""

    class Meta:
        model = User
        fields = ("id", "email", "name", "person_telephone", "surname", "role")
        validators = [UserValidationFields()]
