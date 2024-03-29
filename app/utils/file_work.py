import os

from app.orders.models import OrderFileData
from app.utils.storage import CloudStorage

# from config.settings import BASE_DIR


class FileWork(object):
    """Class for working with uploaded files."""

    def __init__(self, temp_file):
        self.temp_file = temp_file
        # self.dir_path = os.path.join(BASE_DIR, "media_type")
        # self.filename = temp_file.split("/")[-1]
        self.upload_file_size = self._upload_file_size()
        # self.preview_file_size = self._preview_file_size()

    # def preview_path(self):
    #     """Preparing preview path"""
    #     return os.path.join(
    #         "media_type", f"{self.temp_file.split('.')[-1]}_thumbnails.jpg"
    #     )

    def _upload_file_size(self):
        """Calculating the file size."""
        return os.path.getsize(self.temp_file)

    # def _preview_file_size(self):
    #     """Calculating the preview file size"""
    #     return os.path.getsize(os.path.join(BASE_DIR, self.preview_path()))

    @staticmethod
    def get_download_file_link(file: OrderFileData):
        """
        Получение прямой ссылки на скачивание файла на основе id файла
        из БД
        :param file: объект модели OrderFileData
        """

        yandex = CloudStorage()
        yandex_path = file.yandex_path
        download_link = yandex.cloud_get_file(yandex_path)["download_url"]

        return download_link
