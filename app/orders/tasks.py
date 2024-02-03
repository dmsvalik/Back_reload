import os

from app.orders.utils.files import (
    copy_order_file,
    update_order_file_data,
    moving_order_files_to_user,
)
from app.questionnaire.models import Question
from app.questionnaire.serializers import FileSerializer
from app.utils.file_work import FileWork
from app.utils.image_work import GifWork, ImageWork
from celery.utils.log import get_task_logger
from app.utils.storage import CloudStorage

from celery import shared_task
from rest_framework import status

from app.orders.models import OrderFileData, OrderModel
from config.settings import BASE_DIR

logger = get_task_logger(__name__)


# celery -A config.celery worker


@shared_task
def celery_delete_file_task(file_id: int):
    """
    Удаление файла с ЯД.
    file_id: int - id модели OrderFileData
    """
    try:
        file_to_delete = OrderFileData.objects.get(id=file_id)
        yandex = CloudStorage()
        if file_to_delete.yandex_path:
            yandex.cloud_delete_file(file_to_delete.yandex_path)

        file_to_delete.delete()

        logger.info(f"Файл с id {file_id} успешно удален.")
        return {"status": "SUCCESS", "response": "Файл удален"}
    except OrderFileData.DoesNotExist:
        logger.error(f"Файл с id {file_id} не найден.")
        return {
            "status": "FAILURE",
            "response": f"Файл с id {file_id} не найден.",
        }

    except Exception as e:
        logger.error(f"Ошибка при удалении файла с id {file_id}: {e}")
        return {
            "status": "FAILURE",
            "response": f"Ошибка при удалении файла с id {file_id}",
        }


@shared_task
def celery_delete_image_task(file_id: int):
    """
    Удаление изображения с сервера и ЯД.
    file_id: int - id модели OrderFileData
    """
    try:
        file_to_delete = OrderFileData.objects.get(id=file_id)
        yandex = CloudStorage()
        preview_path = file_to_delete.server_path
        if file_to_delete.yandex_path:
            yandex.cloud_delete_file(file_to_delete.yandex_path)
        if preview_path:
            full_preview_path = os.path.join(BASE_DIR, "files/", preview_path)
            if os.path.exists(full_preview_path):
                os.remove(full_preview_path)
        file_to_delete.delete()
        logger.info(f"Файл с id {file_id} успешно удален.")
        return {"status": "SUCCESS", "response": "Файл удален"}
    except OrderFileData.DoesNotExist:
        logger.error(f"Файл с id {file_id} не найден.")
        return {
            "status": "FAILURE",
            "response": f"Файл с id {file_id} не найден.",
        }

    except Exception as e:
        logger.error(f"Ошибка при удалении файла с id {file_id}: {e}")
        return {
            "status": "FAILURE",
            "response": f"Ошибка при удалении файла с id {file_id}",
        }


@shared_task()
def celery_upload_image_task_to_answer(
    temp_file: str,
    order_id: int,
    user_id: int | None,
    question_id: int,
    original_name: str,
):
    """
    Загрузка изображения на ЯД, создание превью картинки и сохранение ее на
    сервере.
    temp_file: str - адрес временного файла сохраненного в папке tmp,
    order_id: int - id заказа к которому крепится изображение,
    user_id: int | None - id пользователя прикреплюящего изображение,
    может быть None,
    question_id: int - id вопроса к которому прилагается изображения,
    original_name: str - изначальное имя изображения переданного пользователем
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
            serializer = FileSerializer(instance=created_file)
            return {"status": "SUCCESS", "response": serializer.data}
        else:
            if os.path.exists(image.preview_path):
                os.remove(image.preview_path)
            os.remove(image.temp_file)
            return {
                "status": "FAILURE",
                "response": f"Ошибка при загрузке файла: {result}",
            }
    except OrderModel.DoesNotExist:
        return {"status": "FAILURE", "response": "Заказ не найден."}
    except Question.DoesNotExist:
        return {"status": "FAILURE", "response": "Вопрос не найден."}
    except Exception as e:
        return {"status": "FAILURE", "response": f"Ошибка: {str(e)}"}


@shared_task()
def celery_upload_file_task_to_answer(
    temp_file: str,
    order_id: int,
    user_id: int | None,
    question_id: int,
    original_name: str,
):
    """
    Загрузка файла на ЯД, создание превью картинки и сохранение ее на сервере.
    temp_file: str - адрес временного файла сохраненного в папке tmp,
    order_id: int - id заказа к которому крепится файл,
    user_id: int | None - id пользователя прикреплюящего файл, может быть None,
    question_id: int - id вопроса к которому прилагается файл,
    original_name: str - изначальное имя файла переданного пользователем
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
            serializer = FileSerializer(instance=created_file)
            return {"status": "SUCCESS", "response": serializer.data}
        else:
            os.remove(file.temp_file)
            return {
                "status": "FAILURE",
                "response": f"Ошибка при загрузке файла: {result}",
            }
    except OrderModel.DoesNotExist:
        return {"status": "FAILURE", "response": "Заказ не найден."}
    except Question.DoesNotExist:
        return {"status": "FAILURE", "response": "Вопрос не найден."}
    except Exception as e:
        return {"status": "FAILURE", "response": f"Ошибка: {str(e)}"}


@shared_task()
def celery_copy_order_file_task(
    user_id: int, old_order_id: int, new_order_id: int
):
    """
    Метод копирует файлы заказа в папку клонируемого заказа
    @param user_id: id пользователя кому принадлежит заказ
    @param old_order_id: id клонируемого заказа
    @param new_order_id: id нового заказа
    @return: str - id операции копирования
    """
    copy_order_file(user_id, old_order_id, new_order_id)


@shared_task()
def celery_update_order_file_data_tusk(
    order_id: int, operation_id: str, path_to: str, user_id: int
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
    update_order_file_data(order_id, operation_id, path_to, user_id)


@shared_task
def moving_user_order_files_task(user_id: int, order_id: int) -> None:
    """
    Отложенная задача для перемещения файлов пользователя из каталога no_user
    в каталог пользователя.
    @param user_id: id пользователя
    @param order_id: id заказа
    @return:
    """
    moving_order_files_to_user(user_id, order_id)
