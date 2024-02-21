import os
from abc import ABC, abstractmethod
from typing import Any

from app.file.models import FileModel, OfferFileModel
from app.file.storage.server import ServerFiles, ServerImageFiles
from app.file import exception as ex
from app.file.tasks import task_moving_files
from app.orders.models import OrderOffer
from config.settings import FILE_SETTINGS, IMAGE_FILE_FORMATS


class FileWorkBase(ABC):
    """Класс с методами работы с файлами"""

    def __init__(self):
        self._dir = None
        self.relative_path = self._dir

        self._model = FileModel
        self._sub_model = FileModel
        self._server = ServerFiles
        self.instance_id = None

    @staticmethod
    def get_path(*args):
        if len(args) <= 1:
            raise ex.FewElementsError
        return os.path.join(*map(lambda x: str(x), args)).__str__()

    def save_file_db(self, **kwargs):
        file = self._model.objects.create(**kwargs)
        return file

    @abstractmethod
    def _create_bunch(self, file_ids: list[int]):
        pass

    def _moving_files_to_dirobj(self, file_ids: list, user_id: int):
        """Метод перемещает файлы в директорию файлов объекта
        и пересчитывает квоту пользователя"""
        task_moving_files.delay(self.relative_path, file_ids, user_id)

    def create(self, file: Any) -> dict:
        """Метод выполняет сохранение на сервере и возвращает словарь
        с параметрами для сохранения в БД"""

        file_format = self._server.get_file_format(file.name)
        if file_format in IMAGE_FILE_FORMATS:
            self._server = ServerImageFiles

        server = self._server(self.relative_path)
        name = server.get_unique_filename(file.name)
        path = server.generate_path(self.relative_path, name)
        path, size = server.save(path, file)
        data = {
            "original_name": file.name,
            "file_path": path,
            "server_size": size,
            "yandex_size": 0,
        }

        if self._server == ServerImageFiles:
            preview_path, size = server.save_preview(path)
            data["preview_path"] = preview_path
            data["server_size"] += size

        return data

    def get_file_ids(self):
        """Метод возвращает список id файлов принадлежащих объекту"""
        return (
            self._sub_model.objects.select_related("file")
            .filter(pk=self.instance_id)
            .file.values_list("id")
        )

    def binding_files(self, file_ids: list):
        """
        Метод привязывает файлы к сущности,
        @param file_ids:
        @return:
        """
        self._create_bunch(file_ids)

    def update(self):
        pass

    def delete(self):
        pass


class TmpFileWork(FileWorkBase):
    def __init__(self):
        super().__init__()
        self._dir = FILE_SETTINGS.get("PATH_TMP_FILES")
        self.relative_path = self._dir

    def _create_bunch(self, file_ids: list[int]):
        pass


class OfferFileWork(FileWorkBase):
    """Класс с методами работы с файлами оффера"""

    def __init__(self, offer_id: int):
        super().__init__()
        self.instance_id = offer_id
        self.user_id = (
            OrderOffer.objects.select_related("user_account")
            .get(pk=offer_id)
            .user_account.id
        )
        self._dir = os.path.join(
            FILE_SETTINGS.get("PATH_OFFER_FILES")
        ).__str__()

        self.relative_path = self.get_path(
            self._dir, self.user_id, self.instance_id
        )
        self._model = FileModel
        self._sub_model = OfferFileModel

    def _create_bunch(self, file_ids: list[int]):
        """
        Метод создает связь между объектом(оффер)
        и файлами в базе данных
        @param file_ids: список id файлов привязываемых к объекту
        @return:
        """
        create_lst = []
        for file_id in file_ids:
            create_lst.append(
                self._sub_model(offer_id=self.instance_id, file_id=file_id)
            )
        self._sub_model.objects.bulk_create(create_lst)
        self._moving_files_to_dirobj(file_ids, self.user_id)
