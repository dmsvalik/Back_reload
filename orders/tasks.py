import os
import random
import string
from pathlib import Path

from utils.storage import CloudStorage

# from celery import shared_task
from PIL import Image
from rest_framework.response import Response

from config.settings import BASE_DIR
from orders.models import FileData


# @shared_task()
def celery_upload_image_task(temp_file, user_id, order_id):
    dir_path = os.path.join(BASE_DIR, "files", str(user_id), str(order_id))
    filename = _generate_new_filename(dir_path)
    file_path = os.path.join(dir_path, filename)
    preview = _prepare_and_save_preview_image(temp_file, file_path)
    prepared_temp_file = _prepare_image_before_upload(temp_file)
    yandex = CloudStorage()
    result = yandex.cloud_upload_image(temp_file, user_id, order_id, prepared_temp_file)
    if result['status_code'] == 201:
        FileData.objects.create(
            user_account=user_id,
            order_id=order_id,
            yandex_path=result['yandex_path'],
            server_path=preview,
            yandex_size=os.path.getsize(prepared_temp_file),
            server_size=os.path.getsize(file_path)
        )

        return Response({"status": "success"})
    return Response(
        {
            "status": "failed",
            "message": f"Unexpected response from Yandex.Disk: {result['status_code']}",
        },
    )


def _prepare_catalog_file_names(dir_path):
    """Функция список всех имен файлов в каталоге заказа пользователя"""
    res = []
    if Path(dir_path).is_dir():
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                filename = path.split('.')[0]
                res.append(filename)
    else:
        os.makedirs(dir_path)
    return res


def _generate_new_filename(dir_path):
    existed_names = _prepare_catalog_file_names(dir_path)
    generated_file_name = ''.join(random.choices(
        string.ascii_letters + string.digits, k=7
    ))
    while generated_file_name in existed_names:
        generated_file_name = ''.join(random.choices(
            string.ascii_letters + string.digits, k=7
        ))
    return f'{generated_file_name}.jpg'


def _prepare_and_save_preview_image(image, file_path):
    img = Image.open(image)
    img.thumbnail((300, 300))
    img.save(file_path)
    return file_path


def _prepare_image_before_upload(image):
    image_size = os.path.getsize(image)
    img = Image.open(image)
    new_size_ratio = 0.9
    while image_size > 1048576:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)))
        img.save(image)
        image_size = os.path.getsize(image)
    return img
