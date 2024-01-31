from django.utils import timezone
from django.http import QueryDict
from django.utils.decorators import method_decorator

from drf_yasg.openapi import Schema
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from datetime import timedelta, datetime
import json
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict

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


def save_many_obj_to_db(
    model: Any, data_lst: List[Dict], **kwargs: Any
) -> None:
    """
    Метод выполняет множественное сохранение однотипных объектов в БД
    @param model: модель для сохранения объекта
    @param data_lst: list - данные в виде списка словарей
    @param kwargs: Any - любые общие данные для группы сохраняемых экземпляров
    (важно: эти данные не должны быть прописаны в словаре экземпляра)
    @return:
    """
    obj_lst = []
    for data in data_lst:
        obj_lst.append(model(**data, **kwargs))
    model.objects.bulk_create(obj_lst)


def create_celery_beat_task(
    order_id: int, operation_id: str, path_to: str, user_id: int
):
    """
    Метод создает отложенную задачу для проверки статуса копирования файлов
    @param order_id: id заказа.
    @param operation_id: - ссылка на проверку статуса заказа яндекс API
    @param path_to: путь до файлов заказа
    @param user_id: id пользователя
    @return: None
    """
    data = {
        "operation_id": operation_id,
        "path_to": path_to,
        "user_id": user_id,
        "order_id": order_id,
    }
    schedule, create = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.MINUTES
    )
    PeriodicTask.objects.create(
        name=f"update_files_{order_id}",
        task="app.orders.tasks.celery_update_order_file_data_tusk",
        interval=schedule,
        kwargs=json.dumps(data),
        start_time=datetime.now(timezone.utc) + timedelta(minutes=1),
    )
