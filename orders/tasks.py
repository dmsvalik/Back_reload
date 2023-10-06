import os

from utils import errorcode
from utils.image_work import GifWork, ImageWork
from utils.storage import CloudStorage
from utils.views import recalculate_quota

from celery import shared_task
from rest_framework import status
from rest_framework.response import Response

from main_page.models import UserAccount
from orders.models import FileData, OrderModel


# celery -A config.celery worker


@shared_task()
def celery_upload_image_task(temp_file, user_id, order_id):
    """Task to write a file on the server and
    create a preview of the image to it."""
    if not UserAccount.objects.filter(id=user_id).exists() or not OrderModel.objects.filter(id=order_id).exists():
        raise errorcode.IncorrectImageOrderUpload()
    file_format = temp_file.split('.')[-1]
    if file_format != 'gif':
        image = ImageWork(temp_file, user_id, order_id)
    else:
        image = GifWork(temp_file, user_id, order_id)
    yandex = CloudStorage()
    result = yandex.cloud_upload_image(image.temp_file, image.user.id, image.order.id,
                                       image.filename)
    if result['status_code'] == status.HTTP_201_CREATED:
        FileData.objects.create(
            user_account=image.user,
            order_id=image.order,
            yandex_path=result['yandex_path'],
            server_path=image.preview_path,
            yandex_size=image.upload_file_size,
            server_size=image.preview_file_size
        )
        os.remove(image.temp_file)
        recalculate_quota(image.user, image.upload_file_size, image.preview_file_size)
        return Response({"status": "success"})
        # If an error occurs, we delete temp files and preview
    os.remove(image.temp_file)
    os.remove(image.preview_path)
    return Response(
        {
            "status": "failed",
            "message": f"Unexpected response from Yandex.Disk: {result['status_code']}",
        },
    )
