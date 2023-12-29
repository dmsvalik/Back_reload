from django.core.validators import validate_email
from rest_framework import serializers
import string


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
                        "error": "Телефон должен начинаться с +7, иметь 12 знаков(цифры)."
                    }
                )

        if self.name in value:
            # если надо сделать уникальным поменяй в модели unique=True - это для channels
            if len(value[self.name]) <= 2 or len(value[self.name]) >= 50:
                raise serializers.ValidationError(
                    {"error": "Не корретное количество букв в имени"}
                )

            if any(x for x in string.punctuation if x in value[self.name]):
                raise serializers.ValidationError(
                    {"error": "не допустимые символы в имени!"}
                )

        if self.surname in value:
            # если надо сделать уникальным поменяй в модели unique=True - это для channels
            if len(value[self.surname]) <= 2 or len(value[self.surname]) >= 50:
                raise serializers.ValidationError(
                    {"error": "Не корретное количество букв в имени"}
                )

            if any(x for x in string.punctuation if x in value[self.surname]):
                raise serializers.ValidationError(
                    {"error": "не допустимые символы в имени!"}
                )

            if self.email in value:
                validate_email(value[self.email])
