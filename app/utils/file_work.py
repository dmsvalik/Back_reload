import os

from app.orders.models import OrderFileData
from app.utils.storage import CloudStorage
from config.settings import BASE_DIR

from django.shortcuts import get_object_or_404


class FileWork(object):
    """Class for working with uploaded files."""

    def __init__(self, temp_file):

        self.temp_file = temp_file
        self.dir_path = os.path.join(BASE_DIR, "media_type")
        self.filename = temp_file.split('/')[-1]
        self.upload_file_size = self._upload_file_size()
        self.preview_file_size = self._preview_file_size()

    def preview_path(self):
        """Preparing preview path"""
        return os.path.join(self.dir_path, f"{self.temp_file.split('.')[-1]}_thumbnails.jpg")

    def _upload_file_size(self):
        """Calculating the file size."""
        return os.path.getsize(self.temp_file)

    def _preview_file_size(self):
        """Calculating the preview file size"""
        return os.path.getsize(self.preview_path())


    @staticmethod
    def get_download_file_link(file_id: int, file_model=OrderFileData) -> str:
        """
        Получение прямой ссылки на скачивание файла на основе id файла
        из БД
        :param file_id: id файла в БД
        :param file_model: Модель в БД
        :return: Ссылка на скачивание файла
        """

        file_data = get_object_or_404(file_model, id=file_id)
        yandex = CloudStorage()
        yandex_path = file_data.yandex_path
        download_link = yandex.cloud_get_file(yandex_path)['download_url']

        return download_link
