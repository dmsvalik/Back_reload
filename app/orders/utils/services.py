from django.utils import timezone
from django.http import QueryDict
from django.utils.decorators import method_decorator

from drf_yasg.openapi import Schema

from datetime import timedelta, datetime

from app.orders.constants import OfferState, OrderState
from app.orders.models import OrderOffer, OrderModel


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


def select_offer(obj: OrderOffer, status: str | None) -> None:
    """
    При обновлении статуса оффера на selected
    Меняет все статусы всех остальных офферов
    которые связаны с эти заказом на archive
    """
    if status != OfferState.SELECTED.value:
        return  # TODO: raise exception
    offers_order = (
        OrderOffer.objects.filter(order_id=obj.order_id)
        .exclude(pk=obj.pk)
        .all()
    )
    for offer in offers_order:
        offer.status = OfferState.ARCHIVE.value
    OrderOffer.objects.bulk_update(offers_order, fields=["status"])
    OrderModel.objects.filter(pk=obj.order_id.pk).update(
        state=OrderState.SELECTED.value
    )
