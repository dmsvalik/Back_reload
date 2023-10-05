import os
import random
import string
from pathlib import Path

from utils import errorcode
from utils.storage import CloudStorage
from utils.views import recalculate_quota

from celery import shared_task
from PIL import Image, ImageSequence
from rest_framework import status
from rest_framework.response import Response

from config.settings import BASE_DIR
from main_page.models import UserAccount
from orders.models import FileData, OrderModel


# celery -A config.celery worker

MAX_IMAGE_SIZE_IN_B = 1048576
MAXIMUM_DIMENSIONS_OF_SIDES = (300, 300)
COEFFICIENT_OF_SIZE_CHANGING = 0.9
COEFFICIENT_OF_GIF_SIZE_CHANGING = 0.7
NUMBER_OF_CHARACTERS_IN_FILENAME = 7


@shared_task()
def celery_upload_image_task(temp_file, user_id, order_id):
    """Task to write a file on the server and
    create a preview of the image to it."""
    # Generate a name and create a path to store the preview image
    file_format = temp_file.split('.')[-1]
    dir_path = os.path.join(BASE_DIR, "files", str(user_id), str(order_id))
    filename = _generate_new_filename(dir_path, file_format)
    file_path = os.path.join(dir_path, filename)

    # Checking that the user and the order exist
    if not UserAccount.objects.filter(id=user_id).exists() or not OrderModel.objects.filter(id=order_id).exists():
        raise errorcode.IncorrectImageOrderUpload()
    user = UserAccount.objects.get(id=user_id)
    order = OrderModel.objects.get(id=order_id)

    if file_format != 'gif':
        # Reducing the size of the image or animation and saving it as a preview
        preview = _prepare_and_save_preview_image(temp_file, file_path)

        # Preparing an image for uploading to Yandex Disk.
        prepared_temp_file = _prepare_image_before_upload(temp_file)
    else:
        preview = _prepare_and_save_preview_gif(temp_file, file_path)
        prepared_temp_file = _prepare_gif_before_upload(temp_file)

    yandex = CloudStorage()
    result = yandex.cloud_upload_image(prepared_temp_file, user_id, order_id,
                                       filename)

    if result['status_code'] == status.HTTP_201_CREATED:
        yandex_size = os.path.getsize(prepared_temp_file)
        server_size = os.path.getsize(file_path)
        FileData.objects.create(
            user_account=user,
            order_id=order,
            yandex_path=result['yandex_path'],
            server_path=preview,
            yandex_size=yandex_size,
            server_size=server_size
        )
        # delete tmp files
        os.remove(prepared_temp_file)
        recalculate_quota(user, yandex_size, server_size)
        return Response({"status": "success"})
    # If an error occurs, we delete temp files and preview
    os.remove(prepared_temp_file)
    os.remove(file_path)
    return Response(
        {
            "status": "failed",
            "message": f"Unexpected response from Yandex.Disk: {result['status_code']}",
        },
    )


def _prepare_catalog_file_names(dir_path):
    """Parsing a list of all file names in the user's order directory."""
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


def _generate_new_filename(dir_path, file_format):
    """File Name generation."""
    existed_names = _prepare_catalog_file_names(dir_path)
    generated_file_name = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=NUMBER_OF_CHARACTERS_IN_FILENAME
    ))
    while generated_file_name in existed_names:
        generated_file_name = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=NUMBER_OF_CHARACTERS_IN_FILENAME
        ))
    if file_format == 'gif':
        return f'{generated_file_name}.gif'
    return f'{generated_file_name}.jpg'


def _prepare_and_save_preview_image(image, file_path):
    """Reducing the size of the image and saving it as a preview.
    The dimensions of the sides are no more than the established."""
    img = Image.open(image)
    img.thumbnail(MAXIMUM_DIMENSIONS_OF_SIDES)
    img.save(file_path)
    return file_path


def _prepare_and_save_preview_gif(gif, file_path):
    """Reducing the size of the animation image and saving it as a preview.
    The dimensions of the sides are no more than the established."""
    # список для обработанных фреймов
    frames = []
    # откроем файл который создали ранее
    with Image.open(gif) as img:
        for frame in ImageSequence.Iterator(img):
            if frame.size[0] >= frame.size[1]:
                reduction_ratio = 300 / frame.size[0]
            else:
                reduction_ratio = 300 / frame.size[1]
            # и уменьшим согласно коэффициента
            size = (int(frame.size[0] * reduction_ratio), int(frame.size[1] * reduction_ratio))
            frame = frame.resize(size)
            # добавляем обраборанный фрейм в список
            frames.append(frame)

    # сохраняем обработанное GIF-изображение
    frames[0].save(file_path, save_all=True, loop=0,
                   append_images=frames[1:], optimize=False, duration=3)
    return file_path


def _prepare_image_before_upload(image):
    """Preparing an image for uploading to Yandex Disk.
    The image file size is not more than 1 MB."""
    image_size = os.path.getsize(image)
    img = Image.open(image)
    while image_size > MAX_IMAGE_SIZE_IN_B:
        img = img.resize(
            (int(img.size[0] * COEFFICIENT_OF_SIZE_CHANGING),
             int(img.size[1] * COEFFICIENT_OF_SIZE_CHANGING))
        )
        img.save(image)
        image_size = os.path.getsize(image)
    return image


def _prepare_gif_before_upload(gif):
    gif_size = os.path.getsize(gif)
    while gif_size > MAX_IMAGE_SIZE_IN_B:
        frames = []
        # откроем файл который создали ранее
        with Image.open(gif) as img:
            for frame in ImageSequence.Iterator(img):
                # и уменьшим согласно коэффициента
                size = (int(frame.size[0] * COEFFICIENT_OF_GIF_SIZE_CHANGING),
                        int(frame.size[1] * COEFFICIENT_OF_GIF_SIZE_CHANGING))
                frame = frame.resize(size)
                # добавляем обраборанный фрейм в список
                frames.append(frame)

        # сохраняем обработанное GIF-изображение
        frames[0].save(gif, save_all=True, loop=0,
                       append_images=frames[1:], optimize=False, duration=3)
        gif_size = os.path.getsize(gif)
    return gif
