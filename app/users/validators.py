from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible
from django.contrib.auth.password_validation import validate_password

from abc import ABC, abstractmethod
import re
from string import digits


class BaseFieldValidator(ABC):
    """Валидатор для полей модели"""

    @abstractmethod
    def __call__(self, value: str):
        """Реализовать у наследников с логикой валидации"""
        ...


@deconstructible
class PasswordFieldValidator(BaseFieldValidator):
    def __call__(self, password: str):
        validate_password(password)
        self._has_digit(password)

    def _has_digit(self, value: str):
        if not set(value).intersection(set(digits)):
            raise ValidationError("Поле должно содержать хотя бы 1 цифру")


@deconstructible
class NameFieldValidator(BaseFieldValidator):
    MIN_LENGTH = 2

    def __init__(self, min_length: str = None):
        self.min_legnth = min_length if min_length else self.MIN_LENGTH

    def __call__(self, name: str):
        min_validator = MinLengthValidator(
            self.min_legnth,
            f"Длинна поля должна быть не меннее {self.min_legnth} символов",
        )

        min_validator(name)
        self._letter_validate(name)

    def _letter_validate(self, value: str):
        result = re.match(r"^[a-zA-Zа-яёЁА-Я\s\-]+$", value)
        if not result:
            raise ValidationError(
                "Поле должно содержать только сиволы русского либо английского алфавита"
            )
