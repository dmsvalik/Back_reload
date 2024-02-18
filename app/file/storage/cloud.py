import json
import os
import requests

from .mixin import WorkFilePathMixin
from config.settings import TOKEN
from app.file import exception as ex


class CloudBase(WorkFilePathMixin):
    """Базовый класс для работы с файлами через API Yandex Cloud"""

    def __init__(self, path: str = None, overwrite: bool = True):
        self.token = (TOKEN,)
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token[0]}",
        }
        self.overwrite = overwrite
        self.dir_path = self._check_or_create(path) if path else None
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

    def _get_upload_link(self, path: str):
        """
        Метод для создания ссылки для загрузки.
        """
        params = {"path": path, "overwrite": self.overwrite}
        res = requests.get(
            f"{self.URL}/upload", headers=self.headers, params=params
        )
        result = json.loads(res.content)
        try:
            return result["href"]
        except KeyError:
            raise ex.CloudError(result.get("message"))

    def upload_file(self, dir_path: str, filename: str, file) -> str:
        if self.dir_path != dir_path:
            self.dir_path = self._check_or_create(dir_path)

        if not self.dir_path:
            raise ex.CloudError("Не указана ссылка для загрузки")

        full_path = self.generate_path(self.dir_path, filename)
        upload_link = self._get_upload_link(full_path)
        response = requests.put(upload_link, headers=self.headers, data=file)

        if response.status_code == 201:
            return full_path
        else:
            raise ex.CloudError(
                response.json().get(
                    "message", "Возникла ошибка при загрузке файла"
                )
            )


class Cloud(CloudBase):
    def __init__(self, path: str = None, overwrite: bool = True):
        super().__init__(path, overwrite)
