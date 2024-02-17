import string

from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from config.settings import NOTIFICATION_CLASSES
from .constants import ErrorMessages


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    person_telephone = PhoneNumberField()

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


class UserAccountSerializerRead(serializers.ModelSerializer):
    """Сериализатор вывода и обновления данных о пользователе."""

    notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "person_telephone",
            "surname",
            "role",
            "notifications",
        )
        read_only_fields = ("id", "role", "notifications")

    def get_notifications(self, obj):
        return obj.usernotifications_set.values_list(
            "notification_type", flat=True
        )


class UserAccountSerializer(serializers.ModelSerializer):
    """Сериализатор вывода и обновления данных о пользователе."""

    notifications = serializers.MultipleChoiceField(
        choices=[*NOTIFICATION_CLASSES], allow_null=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "person_telephone",
            "surname",
            "role",
            "notifications",
        )
        read_only_fields = ("id", "role", "notifications")

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

    def to_representation(self, instance):
        return UserAccountSerializerRead(instance).data
