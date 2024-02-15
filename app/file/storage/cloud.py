import os
import requests

from config.settings import TOKEN


class CloudBase(object):
    """Базовый класс для работы с файлами через API Yandex Cloud"""

    def __init__(self, overwrite: bool = True):
        self.token = (TOKEN,)
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token[0]}",
        }
        self.overwrite = overwrite
        self.dirs = None

    def upload(self):
        """Метод загрузки файла на Yandex Cloud"""
        pass

    def download(self):
        """Метод скачивания файла с Yandex Cloud"""
        pass

    def _create_path(self, path: str) -> bool or str:
        """
        Метод для создания каталога по пути "path"
        Если каталог не создан, вернуть False
        Иначе: вернуть путь к созданному каталогу
        """
        params = {"path": path}

        response = requests.put(self.URL, headers=self.headers, params=params)
        if response.status_code == 201:
            return path
        elif "error" in response.json():
            return False

    def _check_path(self, path: str) -> bool or str:
        """Метод проверки существования директории на Yandex Cloud"""

        params = {"path": path, "overwrite": self.overwrite}

        res = requests.get(f"{self.URL}", headers=self.headers, params=params)
        res = res.json()

        if "error" in res:
            return False

        return res["path"]

    def _check_or_create(self, path: str) -> bool or str:
        """
        Метод проверяет существование указанной директории,
        и если её нет, то создает.
        @param path: Путь
        @return: bool
        """
        state = self._check_path(path)
        if not state:
            dirs = path.split("/")
            if len(dirs) > 1:
                self._check_or_create(str(os.path.join(*dirs[0:-1])))
            path = self._create_path(path)
        return path

    def get_path(self, *args):
        """Метод генерации пути на Yandex Cloud"""

        if len(args) > 1:
            path = str(os.path.join(*args))
        else:
            path = str(args[0]) + "/"

        return self._check_or_create(path)
