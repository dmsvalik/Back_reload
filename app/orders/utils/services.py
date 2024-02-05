from django.utils import timezone
from django.utils.decorators import method_decorator

from drf_yasg.openapi import Schema
from django_celery_beat.models import PeriodicTask, IntervalSchedule

import json
from datetime import datetime, timedelta
from typing import Any, List, Dict

from app.orders.constants import OfferState, OrderState
from app.orders.models import OrderOffer, OrderModel


def range_filter(hours: int) -> datetime:
    """
    Текущее время минус переданное значение в часах
    """
    result = timezone.now() - timedelta(hours=hours)
    return result


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


def select_offer(obj: OrderOffer) -> None:
    """
    При обновлении статуса оффера на selected
    Меняет все статусы всех остальных офферов
    которые связаны с эти заказом на archive
    """
    # offer to selected
    OrderOffer.objects.filter(pk=obj.pk).update(
        status=OfferState.SELECTED.value
    )
    offers_order = (
        OrderOffer.objects.filter(order_id=obj.order_id)
        .exclude(pk=obj.pk)
        .all()
    )
    # other offers to rejecred
    for offer in offers_order:
        offer.status = OfferState.REJECTED.value
    OrderOffer.objects.bulk_update(offers_order, fields=["status"])
    # order to selected
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


def last_contactor_key_offer(order_id: int) -> int:
    last_offer = OrderOffer.objects.filter(order_id=order_id).last()
    if not last_offer:
        return 0
    return last_offer.contactor_key
