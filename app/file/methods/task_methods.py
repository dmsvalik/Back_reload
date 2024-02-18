from django.contrib.auth import get_user_model
from django.db.models import F

from app.file.models import FileModel
from app.file.storage.cloud import Cloud
from app.file.storage.server import ServerFiles

User = get_user_model()


class TaskFile:
    """Набор универсальных методов работы с файлами для CeleryTask"""

    def __init__(self, user_id: int = None):
        self.server = ServerFiles()
        self.cloud = Cloud()
        self._file_model = FileModel
        # self.user = User.objects.get(pk=user_id) Предполагается для квоты

    def moving_files_to_cloud(self, path_to_save: str, file_ids: list[int]):
        """
        Метод переносит файлы с диска на YandexCloud
        @param path_to_save: Путь сохранения на YandexCloud
        @param file_ids: Список id файлов для переноса
        @return:
        """

        files = self._file_model.objects.filter(id__in=file_ids)
        self.cloud = Cloud(path=path_to_save)

        for file in files:
            file_path = file.file_path

            if self.server.check_path(file_path):
                cloud_path, size = self.upload_to_cloud(
                    path_to_save, file_path
                )

                file.file_path = cloud_path
                file.yandex_size = size
                file.server_size = F("server_size") - size
                file.save()
                self.server.delete(file_path)
            else:
                continue

    def upload_to_cloud(self, path_to_save: str, server_path: str):
        """
        Метод загружает файл с диска на YandexCloud
        @param path_to_save: путь сохранения
        @param server_path: путь файла на сервере
        @return: кортеж (путь на Cloud, размер файла)
        """

        size = self.server.get_size(server_path)
        file_name = self.server.get_filename_from_path(server_path)
        abs_path = self.server.generate_abspath(server_path)
        with open(abs_path, "rb") as file:
            cloud_path = self.cloud.upload_file(path_to_save, file_name, file)
        return cloud_path, size

    def moving_file_to_server(self, path_to_save: str, file_ids: list[int]):
        """
        Метод переносит превью файлы в указанную директорию на сервере
        @param path_to_save: Путь сохранения
        @param file_ids: Список id файлов для переноса
        @return:
        """
        files = self._file_model.objects.filter(id__in=file_ids).exclude(
            preview_path=""
        )
        for file in files:
            file_path = file.preview_path

            if self.server.check_path(file_path):
                abs_path = self.server.generate_abspath(file_path)
                new_preview_path = self.server.moving_file(
                    abs_path, path_to_save
                )
                file.preview_path = new_preview_path
                file.save()
