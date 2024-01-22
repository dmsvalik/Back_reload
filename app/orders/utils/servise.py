from typing import Any, List, Dict


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
