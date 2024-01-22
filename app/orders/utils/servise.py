import json
from datetime import datetime, timedelta
from typing import Any, List, Dict
from django_celery_beat.models import PeriodicTask, IntervalSchedule


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
        start_time=datetime.now() + timedelta(minutes=1),
    )
