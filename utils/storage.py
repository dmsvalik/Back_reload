"""
    Логика для работы с сохранением на сервер / облако / yandex disk.

"""

import os
import json
import requests
import random
import string

from utils import errorcode
from config.settings import TOKEN
from config.settings import BASE_DIR
from main_page.models import UserAccount
from pathlib import Path


class ServerFileSystem:
    NUMBER_OF_CHARACTERS_IN_FILENAME = 7

    def __init__(self, file_name, user_id, order_id=None):

        # there may be documents without an order, in this case we save them in a special folder
        if order_id is None:
            order_id = 'no_order'

        self.user = UserAccount.objects.get(id=user_id)
        self.file_format = file_name.split('.')[-1]
        self.dir_path = os.path.join(BASE_DIR, "files", str(self.user.id), str(order_id))
        self.filename = self.generate_new_filename

    def _prepare_catalog_file_names(self, dir_path):
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

    def generate_new_filename(self):
        """File Name generation for differents documents (images, pdf ...)"""

        existed_names = self._prepare_catalog_file_names(self.dir_path)
        generated_file_name = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=self.NUMBER_OF_CHARACTERS_IN_FILENAME
        ))
        while generated_file_name in existed_names:
            generated_file_name = ''.join(random.choices(
                string.ascii_letters + string.digits,
                k=self.NUMBER_OF_CHARACTERS_IN_FILENAME
            ))

        return f'{generated_file_name}.{self.file_format}'


class CloudStorage:
    def __init__(self):
        self.token = TOKEN,
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token[0]}",
        }
        self.overwrite = "true"

    def _check_path(self, path):
        """
        Метод для проверки существования папки по указанному пути.
        """
        params = {"path": path, "overwrite": self.overwrite}
        res = requests.get(f"{self.URL}", headers=self.headers, params=params)
        res = res.json()
        if "error" in res:
            return False
        return res["path"]

    def _create_path(self, path):
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
            print(response.json()["message"])
        return False

    def _ensure_path_exists(self, user_id, order_id):
        """
        Метод для создания пути для файла, если он еще не существует.
        """
        path = f"{user_id}/{order_id}"
        user_directory_path = f"{user_id}"
        order_directory_path = f"{user_id}/{order_id}"
        if not self._check_path(order_directory_path):
            if not self._check_path(user_directory_path):
                if not self._create_path(user_directory_path):
                    return False
            if not self._create_path(order_directory_path):
                return False
        return path

    def _get_upload_link(self, path, order_id, name):
        """
        Метод для создания ссылки для загрузки.
        """
        full_path = f"{path}/{name}"
        params = {"path": full_path, "overwrite": self.overwrite}
        res = requests.get(f"{self.URL}/upload", headers=self.headers, params=params)
        result = json.loads(res.content)
        try:
            return result["href"]
        except KeyError:
            return result["message"]

    def cloud_upload_image(self, image, user_id, order_id, name):
        path = self._ensure_path_exists(user_id, order_id)
        if not path:
            print("Failed to create path")
            return False

        upload_link = self._get_upload_link(path, order_id, name)

        with open(image, "rb") as f:
            response = requests.put(upload_link, headers=self.headers, data=f)

        result = dict()
        result['status_code'] = response.status_code
        if response.status_code == 201:
            result['yandex_path'] = path + '/' + name

        return result

    def cloud_get_image(self, yandex_path):
        """
        Метод для получения файла из YandexDisk.
        """

        res = requests.get(f"{self.URL}/download/?path={yandex_path}", headers=self.headers)
        download_url = res.json().get("href")

        if not download_url:
            raise Exception("Failed to get download link for the file.")

        result = {'status': res.status_code,
                  'download_url': download_url}
        return result

    def cloud_delete_image(self, yandex_path):
        """ Метод для удаления файла из YandexDisk."""
        res = requests.delete(
            f"{self.URL}?path={yandex_path}&permanently=True",
            headers=self.headers)
        # если файл на сервере удален или не найден возвращаем True
        if not res.status_code == 204 or not res.status_code == 404:
            raise errorcode.IncorrectImageDeleting
        return True
