import os
import random
import string
from pathlib import Path

from celery import shared_task

from config.settings import MEDIA_ROOT


# from utils.storage import CloudStorage


@shared_task()
def celery_upload_image_task(temp_file_name, user_id, order_id):
    # filename = _generate_new_filename(user_id, order_id)
    # yandex = CloudStorage()
    # response_code = yandex.cloud_upload_image(temp_file_name, user_id, order_id, name)
    pass


def _prepare_catalog_file_names(user_id, order_id):
    """Функция список всех имен файлов в каталоге заказа пользователя"""
    dir_path = f'{MEDIA_ROOT}/{user_id}/{order_id}/'
    res = []
    if Path(dir_path).is_dir():
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                filename = path.split('.')[0]
                res.append(filename)
    return res


def _generate_new_filename(user_id, order_id):
    existed_names = _prepare_catalog_file_names(user_id, order_id)
    generated_file_name = ''.join(random.choices(
        string.ascii_letters + string.digits, k=7
    ))
    while generated_file_name in existed_names:
        generated_file_name = ''.join(random.choices(
            string.ascii_letters + string.digits, k=7
        ))
    return generated_file_name
