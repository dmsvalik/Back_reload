import json
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from app.utils.storage import CloudStorage


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
    name: str, data: dict, task: str, interval: int = 1
) -> None:
    """
    Метод создает новую периодическую задачу
    @param name: Имя задачи
    @param data: Данные необходимые для выполнения метода в задаче
    @param task: Метод выполняемый в задаче
    @param interval: Интервал выполнения в минутах
    @return: None
    """
    schedule, create = IntervalSchedule.objects.get_or_create(
        every=interval, period=IntervalSchedule.MINUTES
    )
    PeriodicTask.objects.create(
        name=name,
        task=task,
        interval=schedule,
        kwargs=json.dumps(data),
        start_time=datetime.now(timezone.utc) + timedelta(minutes=interval),
    )


def update_periodic_tusk_copy(operation_id: str, name: str):
    """
    Метод обновляет периодическую задачу на основе статуса
    возвращенного от API Yandex
    @param operation_id: id операции
    @param name: имя периодической задачи
    @return: статус выполнения операции
    """
    yandex = CloudStorage()
    state = yandex.check_status_operation(operation_id)

    task = PeriodicTask.objects.get(name=name)
    task.total_run_count += 1
    task.save()

    if state == "in-progress" and task.total_run_count < 3:
        return False

    if state == "success":
        task.delete()
        return True
    else:
        task.delete()
        return False
