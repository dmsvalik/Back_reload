from django.core.validators import validate_email
from rest_framework import serializers
import string

from .constants import ErrorMessages


class UserValidationFields:
    """Валидация данных при обновлении пользователя."""

    def __init__(
        self,
        person_telephone="person_telephone",
        name="name",
        surname="surname",
        email="email",
    ):
        self.person_telephone = person_telephone
        self.email = email
        self.name = name
        self.surname = surname

    def __call__(self, value):
        if self.person_telephone in value:
            if (
                value[self.person_telephone][0:2] != "+7"
                or len(value[self.person_telephone]) != 12
                or value[self.person_telephone][1:].isdigit() is False
            ):
                raise serializers.ValidationError(
                    {
                        "person_telephone": ErrorMessages.PHONE_FIELD_VALIDATION_ERROR
                    }
                )

        if self.name in value:
            # если надо сделать уникальным поменяй в модели unique=True - это
            # для channels
            if len(value[self.name]) <= 2 or len(value[self.name]) >= 50:
                raise serializers.ValidationError(
                    {"name": ErrorMessages.WRONG_NUMBER_OF_LETTER}
                )

            if any(x for x in string.punctuation if x in value[self.name]):
                raise serializers.ValidationError(
                    {"name": ErrorMessages.INVALID_CHARACTERS}
                )

        if self.surname in value:
            # если надо сделать уникальным поменяй в модели unique=True - это
            # для channels
            if len(value[self.surname]) <= 2 or len(value[self.surname]) >= 50:
                raise serializers.ValidationError(
                    {"surname": ErrorMessages.WRONG_NUMBER_OF_LETTER}
                )

            if any(x for x in string.punctuation if x in value[self.surname]):
                raise serializers.ValidationError(
                    {"surname": ErrorMessages.INVALID_CHARACTERS}
                )

            if self.email in value:
                validate_email(value[self.email])
