import os
from typing import Any

from app.file.models import FileModel
from app.file.storage.server import ServerFiles, ServerImageFiles
from app.file import exception as ex
from config.settings import FILE_SETTINGS, IMAGE_FILE_FORMATS


class FileWorkBase(object):
    """Класс с методами работы с файлами"""

    def __init__(self):
        self._dir = None
        self._relative_path = self._dir

        self._model = FileModel
        self._sub_model = FileModel
        self._server = ServerFiles

    @staticmethod
    def get_path(*args):
        if len(args) <= 1:
            raise ex.FewElementsError
        return os.path.join(*args).__str__()

    def save_file_db(self, **kwargs):
        file = self._model.objects.create(**kwargs)
        return file

    def create(self, file: Any) -> dict:
        """Метод выполняет сохранение на сервере и возвращает словарь
        с параметрами для сохранения в БД"""

        server = self._server()
        name = server.get_unique_filename(file.name)
        path = server.generate_path(self._relative_path, name)
        path, size = server.save(path, file)
        data = {
            "original_name": file.name,
            "file_path": path,
            "server_size": size,
            "yandex_size": 0,
        }
        file_format = server.get_file_format(name)

        if file_format in IMAGE_FILE_FORMATS:
            image = ServerImageFiles()
            preview_path, size = image.save_preview(path)
            data["preview_path"] = preview_path
            data["server_size"] += size

        return data

    def update(self):
        pass

    def delete(self):
        pass


class TmpFileWork(FileWorkBase):
    def __init__(self):
        super().__init__()
        self._dir = FILE_SETTINGS.get("PATH_TMP_FILES")
        self._relative_path = self._dir


class OfferFileWork(FileWorkBase):
    """Класс с методами работы с файлами оффера"""

    def __init__(self, user_id: int, offer_id: int):
        super().__init__()
        self.dir = os.path.join(
            FILE_SETTINGS.get("PATH_OFFER_FILES")
        ).__str__()

        self.relative_path = self.get_path(self._dir, user_id, offer_id)
        self._model = FileModel
        self._sub_model = None
