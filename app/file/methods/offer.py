import os

from app.file.models import FileModel
from config.settings import FILE_SETTINGS


class FileWorkBase(object):
    """Класс с методами работы с файлами"""

    def __init__(self):
        self._dir = FILE_SETTINGS.get("PATH_TMP_FILES")
        self.relative_path = self._dir

        self._model = FileModel
        self._sub_model = None

    @staticmethod
    def get_path(*args):
        return os.path.join(*args)

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class OfferFileWork(FileWorkBase):
    """Класс с методами работы с файлами оффера"""

    def __init__(self, user_id: int, offer_id: int):
        super().__init__()
        self.relative_path = self.get_path(self._dir, user_id, offer_id)
        self._model = FileModel
        self._sub_model = None
