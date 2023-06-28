import string

from django.core.validators import validate_email
from rest_framework import exceptions


class UserValidationFields:
    def __init__(self, person_telephone='person_telephone', name='name', surname='surname', email='email'):
        self.person_telephone = person_telephone
        self.email = email
        self.name = name
        self.surname = surname

    def __call__(self, value):

        if self.person_telephone in value:
            if (
                    value[self.person_telephone][0:2] != '+7'
                    or len(value[self.person_telephone]) != 12
                    or value[self.person_telephone][1:].isdigit() is False
            ):
                raise exceptions.ValidationError({
                    "person_telephone": "Телефон должен начинаться с +7, иметь 12 знаков(цифры)."})

        if self.name in value:
            # если надо сделать уникальным поменяй в модели unique=True - это для channels
            if len(value[self.name]) <= 2 or len(value[self.name]) >= 50:
                raise exceptions.ValidationError({"name": "Не корретное количество букв в имени"})

            if any(x for x in string.punctuation if x in value[self.name]):
                raise exceptions.ValidationError({"name": "не допустимые символы в имени!"})

        if self.surname in value:
            # если надо сделать уникальным поменяй в модели unique=True - это для channels
            if len(value[self.surname]) <= 2 or len(value[self.surname]) >= 50:
                raise exceptions.ValidationError({"surname": "Не корретное количество букв в имени"})

            if any(x for x in string.punctuation if x in value[self.surname]):
                raise exceptions.ValidationError({"surname": "не допустимые символы в имени!"})

        if self.email in value:
            validate_email(value[self.email])
