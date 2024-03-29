import os

from rest_framework.response import Response
from rest_framework import status


from app.orders.utils.db_data import CloneOrderDB, UpdateOrderDB
from app.orders.utils.servise import (
    create_celery_beat_task,
    update_periodic_tusk_copy,
)

from app.questionnaire.models import Question
from app.questionnaire.serializers import FileSerializer
from app.utils.file_work import FileWork
from app.utils.image_work import GifWork, ImageWork
from app.utils.storage import CloudStorage, OrderServerFiles
from app.utils.errorcode import (
    FileNotFound,
    IncorrectFileDeleting,
    IncorrectFileUploading,
    QuestionIdNotFound,
)
from app.users.utils.quota_manager import UserQuotaManager

# from celery import shared_task

from app.orders.models import OrderFileData, OrderModel
from config.settings import BASE_DIR, FILE_SETTINGS


# celery -A config.celery worker


def delete_file(
    file_id: int,
    quota_manager: UserQuotaManager | None = None,
):
    """
    Удаление файла с ЯД.
    file_id: int - id модели OrderFileData
    quota_manager: UserQuotaManager - обьект для пересчета квоты пользователя
    """
    try:
        file_to_delete = OrderFileData.objects.get(id=file_id)
        yandex = CloudStorage()
        if file_to_delete.yandex_path:
            yandex.cloud_delete_file(file_to_delete.yandex_path)
        file_to_delete.delete()
        if quota_manager:
            quota_manager.subtract(file_to_delete)

        return Response(
            {"response": "Файл удален"}, status=status.HTTP_204_NO_CONTENT
        )
    except OrderFileData.DoesNotExist:
        raise FileNotFound()

    except Exception:
        raise IncorrectFileDeleting()


def delete_image(
    file_id: int,
    quota_manager: UserQuotaManager | None = None,
):
    """
    Удаление изображения с сервера и ЯД.
    file_id: int - id модели OrderFileData
    quota_manager: UserQuotaManager - обьект для пересчета квоты пользователя
    """
    try:
        file_to_delete = OrderFileData.objects.get(id=file_id)
        yandex = CloudStorage()
        preview_path = file_to_delete.server_path
        if file_to_delete.yandex_path:
            yandex.cloud_delete_file(file_to_delete.yandex_path)
        if preview_path:
            full_preview_path = os.path.join(
                BASE_DIR, FILE_SETTINGS.get("PATH_SERVER_FILES"), preview_path
            )
            if os.path.exists(full_preview_path):
                os.remove(full_preview_path)
        file_to_delete.delete()
        if quota_manager:
            quota_manager.subtract(file_to_delete)

        return Response(
            {"response": "Файл удален"}, status=status.HTTP_204_NO_CONTENT
        )
    except OrderFileData.DoesNotExist:
        raise FileNotFound()

    except Exception:
        raise IncorrectFileDeleting()


def upload_image_to_answer(
    temp_file: str,
    order_id: int,
    question_id: int,
    original_name: str,
    quota_manager: UserQuotaManager | None = None,
    user_id: int | None = None,
):
    """
    Загрузка изображения на ЯД, создание превью картинки и сохранение ее на
    сервере.
    temp_file: str - адрес временного файла сохраненного в папке tmp,
    order_id: int - id заказа к которому крепится изображение,
    может быть None,
    question_id: int - id вопроса к которому прилагается изображения,
    original_name: str - изначальное имя изображения переданного пользователем
    quota_manager: UserQuotaManager - обьект для пересчета квоты пользователя
    user_id: int | None - id пользователя прикреплюящего изображение,
    """
    if user_id is None:
        user_id = "no_user"
    try:
        order = OrderModel.objects.get(id=order_id)
        question = Question.objects.get(id=question_id)

        file_format = temp_file.split(".")[-1]
        if file_format != "gif":
            image = ImageWork(temp_file, user_id, order_id)
        else:
            image = GifWork(temp_file, user_id, order_id)
        yandex = CloudStorage()
        result = yandex.cloud_upload_image(
            image.temp_file, user_id, order_id, image.filename
        )
        if result["status_code"] == status.HTTP_201_CREATED:
            created_file = OrderFileData.objects.create(
                order_id=order,
                question_id=question,
                original_name=original_name,
                yandex_path=result["yandex_path"],
                server_path=image.preview_path,
                yandex_size=image.upload_file_size,
                server_size=image.preview_file_size,
            )
            os.remove(image.temp_file)
            if quota_manager:
                quota_manager.add(created_file)

            serializer = FileSerializer(instance=created_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if os.path.exists(image.preview_path):
                os.remove(image.preview_path)
            os.remove(image.temp_file)
            raise IncorrectFileUploading()
    except OrderModel.DoesNotExist:
        raise FileNotFound()
    except Question.DoesNotExist:
        raise QuestionIdNotFound()
    except Exception:
        raise IncorrectFileUploading()


def upload_file_to_answer(
    temp_file: str,
    order_id: int,
    question_id: int,
    original_name: str,
    quota_manager: UserQuotaManager | None = None,
    user_id: int | None = None,
):
    """
    Загрузка файла на ЯД, создание превью картинки и сохранение ее на сервере.
    temp_file: str - адрес временного файла сохраненного в папке tmp,
    order_id: int - id заказа к которому крепится файл,
    question_id: int - id вопроса к которому прилагается файл,
    original_name: str - изначальное имя файла переданного пользователем
    quota_manager: UserQuotaManager - обьект для пересчета квоты пользователя
    user_id: int | None - id пользователя прикреплюящего файл, может быть None,
    """
    if user_id is None:
        user_id = "no_user"
    try:
        order = OrderModel.objects.get(id=order_id)
        question = Question.objects.get(id=question_id)
        file = FileWork(temp_file)
        filename = temp_file.split("/")[-1]
        yandex = CloudStorage()
        result = yandex.cloud_upload_image(
            file.temp_file, user_id, order_id, filename
        )
        if result["status_code"] == status.HTTP_201_CREATED:
            created_file = OrderFileData.objects.create(
                order_id=order,
                question_id=question,
                original_name=original_name,
                yandex_path=result["yandex_path"],
                yandex_size=file.upload_file_size,
                server_size=0,
            )
            os.remove(file.temp_file)
            if quota_manager:
                quota_manager.add(created_file)

            serializer = FileSerializer(instance=created_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            os.remove(file.temp_file)
            raise IncorrectFileUploading()
    except OrderModel.DoesNotExist:
        raise FileNotFound()
    except Question.DoesNotExist:
        raise QuestionIdNotFound()
    except Exception:
        raise IncorrectFileUploading()


def copy_order_file(user_id: int, old_order_id: int, new_order_id: int):
    """
    Метод копирует файлы заказа в папку клонируемого заказа
    @param user_id: id пользователя кому принадлежит заказ
    @param old_order_id: id клонируемого заказа
    @param new_order_id: id нового заказа
    @return: str - id операции копирования
    """
    files = (
        OrderFileData.objects.filter(order_id=old_order_id)
        .exclude(yandex_path="")
        .first()
    )
    if files:
        file = CloudStorage()
        path_from = get_path_dir_from_path_file(files.yandex_path)

        path_to = file.create_order_path(
            user_id=user_id, order_id=new_order_id
        )
        operation_id = file.cloud_copy_files(
            path_to, path_from, overwrite=True
        )

        if type(operation_id) is str:
            data = {
                "operation_id": operation_id,
                "path_to": path_to,
                "user_id": user_id,
                "order_id": new_order_id,
            }
            name = f"copy_files_{new_order_id}"
            task = "app.orders.tasks.celery_update_order_file_data_task"
            create_celery_beat_task(name, data, task)

    server_files = (
        OrderFileData.objects.filter(order_id=old_order_id)
        .exclude(server_path="")
        .first()
    )
    if server_files:
        s_dir_from = get_path_dir_from_path_file(server_files.server_path)
        s_dir_to = OrderServerFiles(user_id=user_id, order_id=new_order_id)
        server_path = s_dir_to.copy_dir_files(
            s_dir_from, s_dir_to.relative_path
        )

        db = CloneOrderDB(order_id=new_order_id, user_id=user_id)
        db.update_order_file_path(server_path, cloud=False)


def update_order_file_data_copy(
    order_id: int,
    operation_id: str,
    path_to: str,
    user_id: int,
):
    """
    Метод запрашивает статус копирования файлов и если копирование завершено
    успешно, обновляет данные в БД.
    @param order_id: id заказа.
    @param operation_id: - ссылка на проверку статуса заказа яндекс API
    @param path_to: путь до файлов заказа
    @param user_id: id пользователя
    @return: None
    """
    state = update_periodic_tusk_copy(
        name=f"copy_files_{order_id}", operation_id=operation_id
    )

    db = CloneOrderDB(order_id=order_id, user_id=user_id)
    if state:
        db.update_order_file_path(path_to, server=False)


def moving_order_files_to_user(user_id: int, order_id: int) -> None:
    """
    Метод перемещает файлы пользователя из каталога no_user в каталог
    файлов пользователя на сервере и YandexDisk.
    @param user_id: id пользователя
    @param order_id: id файлов принадлежащих заказу
    @return: None
    """
    files = (
        OrderFileData.objects.filter(order_id=order_id)
        .exclude(yandex_path="")
        .first()
    )
    if files:
        file = CloudStorage()
        path_from = get_path_dir_from_path_file(files.yandex_path)

        path_to = file.create_order_path(user_id=user_id, order_id=order_id)
        operation_id = file.cloud_copy_files(
            path_to, path_from, overwrite=True
        )

        if type(operation_id) is str:
            data = {
                "operation_id": operation_id,
                "path_to": path_to,
                "user_id": user_id,
                "order_id": order_id,
                "path_from": path_from,
            }
            name = f"move_files_{order_id}"
            task = "app.orders.tasks.celery_update_order_file_data_move_task"
            create_celery_beat_task(name, data, task)

    server_files = (
        OrderFileData.objects.filter(order_id=order_id)
        .exclude(server_path="")
        .first()
    )
    if server_files:
        s_dir_from = get_path_dir_from_path_file(server_files.server_path)
        s_dir_to = OrderServerFiles(user_id=user_id, order_id=order_id)
        server_path = s_dir_to.move_dir_files(
            s_dir_from, s_dir_to.relative_path
        )

        db = UpdateOrderDB(order_id=order_id, user_id=user_id)
        db.update_order_file_path(server_path, cloud=False)


def update_order_file_data_move(
    order_id: int,
    operation_id: str,
    path_to: str,
    user_id: int,
    path_from: str,
):
    """
    Метод запрашивает статус копирования файлов и если копирование завершено
    успешно, обновляет данные в БД.
    @param order_id: id заказа.
    @param operation_id: - ссылка на проверку статуса заказа яндекс API
    @param path_to: путь до файлов заказа
    @param path_from: путь до папки предыдущего хранения
    @param user_id: id пользователя
    @return: None
    """
    state = update_periodic_tusk_copy(
        name=f"move_files_{order_id}", operation_id=operation_id
    )
    db = CloneOrderDB(order_id=order_id, user_id=user_id)
    if state:
        yandex = CloudStorage()
        db.update_order_file_path(path_to, server=False)
        yandex.cloud_delete_file(path_from)


def get_path_dir_from_path_file(full_path: str) -> str:
    """
    Метод получает путь до директории с файлом из полного пути файла
    @param full_path: Путь до файла
    @return:
    """
    path_lst = full_path.split("/")
    del path_lst[-1]
    return "/".join(path_lst)
