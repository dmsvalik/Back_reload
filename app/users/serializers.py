import string

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .constants import ErrorMessages


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

    def validate_name(self, value):
        if any(x for x in string.punctuation if x in value):
            raise serializers.ValidationError(ErrorMessages.INVALID_CHARACTERS)
        return value

    def validate_surname(self, value):
        if any(x for x in string.punctuation if x in value):
            raise serializers.ValidationError(ErrorMessages.INVALID_CHARACTERS)
        return value

    def validate_person_telephone(self, value):
        if (
            value[0:2] != "+7"
            or len(value) != 12
            or value[1:].isdigit() is False
        ):
            raise serializers.ValidationError(
                ErrorMessages.PHONE_FIELD_VALIDATION_ERROR
            )
        return value
