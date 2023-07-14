from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, CurrentUserDefault, HiddenField

from rest_framework.serializers import ModelSerializer

from .models import CooperationOffer, UserAccount
from .validators import field_name_validator, field_phone_validator


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    name = CharField(
        min_length=3,
        max_length=120,
    )
    surname = CharField(
        min_length=3,
        max_length=120,
        required=False,
    )

    @staticmethod
    def validate_name(value):
        field_name_validator(value)
        return value

    @staticmethod
    def validate_surname(value):
        field_name_validator(value)
        return value

    @staticmethod
    def validate_person_telephone(value):
        field_phone_validator(value)
        return value

    class Meta:
        model = User
        fields = ("id", "email", "name", "password", "person_telephone", "surname")


class UserAccountSerializer(UserCreateSerializer):
    class Meta:
        model = UserAccount
        fields = ("id", "email", "name", "person_telephone", "surname")


class CooperationOfferSerializer(ModelSerializer):
    user_account_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = CooperationOffer
        fields = "__all__"
