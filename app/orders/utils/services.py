from django.utils import timezone
from django.http import QueryDict
from django.utils.decorators import method_decorator

from drf_yasg.openapi import Schema

from datetime import timedelta, datetime


def range_filter(hours: int) -> datetime:
    """
    Текущее время минус переданное значение в часах
    """
    result = timezone.now() - timedelta(hours=hours)
    return result


def parse_query_params(params: QueryDict) -> dict:
    """
    Возвращает параметры запроса в виде словаря
    """
    return {k: v for k, v in params.items()}


def register_method(method_set: tuple[tuple[Schema, str]]):
    """
    Регистрирует метод вьюсета для свагерра
    принимает кортеж кортежей с сваггер схемой и названием действия
    """

    def wrapper(obj):
        for method in method_set:
            method_decorator(*method)(obj)
        return obj

    return wrapper
