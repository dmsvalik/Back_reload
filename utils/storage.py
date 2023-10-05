""" логика для работы с сохранением на сервер / облако / yandex disk """
import json
import os
import requests


class CloudStorage:
    def __init__(self):
        self.token = os.environ.get("TOKEN")
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}",
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

        # delete tmp files
        # os.remove(image) - перенесено в таску
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
