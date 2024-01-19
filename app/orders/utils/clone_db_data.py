from typing import Any, List, Dict

from app.orders.models import OrderModel, OrderFileData
from app.questionnaire.models import (
    QuestionResponse,
    QuestionnaireType,
    Question,
)


def clone_order(order_id: int, user: Any) -> int:
    """
    Метод копирует данные ордера.
    @param order_id: id заказа
    @param user: instance пользователя
    @return: id - нового заказа
    """

    old_order = OrderModel.objects.values(
        "name", "order_description", "questionnaire_type"
    ).get(pk=order_id)
    old_order["questionnaire_type"] = QuestionnaireType.objects.get(
        pk=old_order["questionnaire_type"]
    )

    new_order = OrderModel.objects.create(user_account=user, **old_order)
    new_order.save()
    return new_order.pk


def clone_order_question_response(old_order_id: int, new_order_id: int):
    """
    Копирование ответов на вопросы анкеты
    @param old_order_id: id клонируемого заказа
    @param new_order_id: id нового заказа
    @return:
    """
    responses = QuestionResponse.objects.filter(order_id=old_order_id).values(
        "response", "question_id"
    )
    save_many_obj_to_db(QuestionResponse, responses, order_id=new_order_id)


def clone_order_file_data(old_order_id: int, new_order_id: int):
    """
    Копирование информации о файлах в БД
    @param old_order_id: id клонируемого заказа
    @param new_order_id: id нового заказа
    @return:
    """
    files_data = OrderFileData.objects.filter(order_id=old_order_id).values(
        "question_id",
        "original_name",
        "yandex_path",
        "server_path",
        "yandex_size",
        "server_size",
    )
    new_order = OrderModel.objects.get(pk=new_order_id)
    for file in files_data:
        file["question_id"] = Question.objects.get(pk=file["question_id"])
    save_many_obj_to_db(OrderFileData, files_data, order_id=new_order)


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
