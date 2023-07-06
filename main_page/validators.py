from string import digits, punctuation

from rest_framework.exceptions import ValidationError


def field_name_validator(value):
    if any(x for x in punctuation + digits if x in value):
        raise ValidationError("Не допустимые символы!")


def field_phone_validator(value):
    if value[0:2] != '+7' or len(value) != 12:
        raise ValidationError("Телефон должен начинаться с +7, иметь 12 знаков(цифры).")
