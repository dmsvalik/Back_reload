"""
    Логика для работы с сохранением на сервер / облако / yandex disk.

"""

import os
import json
import shutil


import requests
import random
import string

from app.utils import errorcode
from app.utils.errorcode import FileNotFound
from config.settings import TOKEN, FILE_SETTINGS
from config.settings import BASE_DIR
from pathlib import Path


class BaseServerFileWork(object):
    """Базовый класс работы с файлами на сервере"""

    def __init__(self):
        self.server_file_dir = str(
            os.path.join(BASE_DIR, FILE_SETTINGS.get("PATH_SERVER_FILES"))
        )

    def copy_dir_files(self, src_path: str, dst_path: str):
        """
        Метод рекурсивного копирования файлов указанной директории. Если
        директория назначения содержит файл с тем же именем, что и файл в
        исходной директории, файл назначения будет заменен.
        @param src_path: Путь до директории с файлами для копирования
        @param dst_path: Путь до директории в которую копируются файлы
        @return: dst_path
        """
        path_from = os.path.join(self.server_file_dir, src_path)
        if os.path.exists(path_from):
            path_to = os.path.join(self.server_file_dir, dst_path)

            shutil.copytree(str(path_from), str(path_to), dirs_exist_ok=True)
        return dst_path

    def move_dir_files(self, src_path: str, dst_path: str):
        """
        Метод рекурсивного перемещения файлов из указанной директории. Если
        директория назначения содержит файл с тем же именем, что и файл в
        исходной директории, файл назначения будет заменен.
        @param src_path: Путь до директории с файлами для перемещения
        @param dst_path: Путь до директории в которую перемещаются файлы
        @return: dst_path
        """
        path_from = os.path.join(self.server_file_dir, src_path)
        if os.path.exists(path_from):
            path_to = os.path.join(self.server_file_dir, dst_path)
            shutil.move(str(path_from), str(path_to))
        return dst_path


class ServerFileSystem(BaseServerFileWork):
    """Предварительная подготовка файла."""

    NUMBER_OF_CHARACTERS_IN_FILENAME = FILE_SETTINGS[
        "NUMBER_OF_CHARACTERS_IN_FILENAME"
    ]

    def __init__(self, file_name, user_id, order_id=None):
        # there may be documents without an order and user, in this case we
        # save them in a special folder
        super().__init__()
        if order_id is None:
            order_id = "no_order"

        if user_id is None:
            user_id = "no_user"

        # self.user = UserAccount.objects.get(id=user_id)
        self.file_format = file_name.split(".")[-1]
        self.relative_path = str(
            os.path.join(
                FILE_SETTINGS.get("PATH_ORDER_FILES"),
                str(user_id),
                str(order_id),
            )
        )
        self.dir_path = os.path.join(self.server_file_dir, self.relative_path)
        self.filename = self.generate_new_filename()

    def _prepare_catalog_file_names(self, dir_path):
        """Parsing a list of all file names in the user's order directory."""
        res = []
        if Path(dir_path).is_dir():
            for path in os.listdir(dir_path):
                # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    filename = path.split(".")[0]
                    res.append(filename)
        else:
            os.makedirs(dir_path)
        return res

    def generate_new_filename(self):
        """File Name generation for differents documents (images, pdf ...)"""

        existed_names = self._prepare_catalog_file_names(self.dir_path)
        generated_file_name = "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=self.NUMBER_OF_CHARACTERS_IN_FILENAME,
            )
        )
        while generated_file_name in existed_names:
            generated_file_name = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=self.NUMBER_OF_CHARACTERS_IN_FILENAME,
                )
            )

        return f"{generated_file_name}.{self.file_format}"


class OrderServerFiles(BaseServerFileWork):
    """Класс для работы с файлами заказов на сервере"""

    def __init__(self, file_name=None, user_id=None, order_id=None):
        super().__init__()

        if order_id is None:
            order_id = "no_order"

        if user_id is None:
            user_id = "no_user"

        self.relative_path = str(
            os.path.join(
                FILE_SETTINGS.get("PATH_ORDER_FILES"),
                str(user_id),
                str(order_id),
            )
        )
        self.dir_path = os.path.join(self.server_file_dir, self.relative_path)


class OfferServerFiles(BaseServerFileWork):
    """Класс для работы с файлами офферов на сервере"""

    def __init__(self, file_name=None, user_id=None, offer_id=None):
        super().__init__()

        offer_id = offer_id if offer_id else "no_offer"
        user_id = user_id if user_id else "no_user"

        self.relative_path = str(
            os.path.join(
                FILE_SETTINGS.get("PATH_OFFER_FILES"),
                str(user_id),
                str(offer_id),
            )
        )

        self.dir_path = os.path.join(self.server_file_dir, self.relative_path)


class ChatsServerFiles(BaseServerFileWork):
    """Класс для работы с файлами чатов на сервере"""

    def __init__(self, chat_id=None):
        super().__init__()
        self.relative_path = str(
            os.path.join(FILE_SETTINGS.get("PATH_OFFER_FILES"), str(chat_id))
        )

        self.dir_path = os.path.join(
            self.server_file_dir,
            FILE_SETTINGS.get("PATH_CHATS_FILES"),
            self.relative_path,
        )


class CloudStorage:
    """Класс для работы с YandexDisk."""

    def __init__(self):
        self.token = (TOKEN,)
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token[0]}",
        }
        self.overwrite = "true"
        self.dir_path = FILE_SETTINGS.get("PATH_ORDER_FILES")

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

    def _ensure_path_exists(
        self, user_id: int or str, order_id: int, not_check=False
    ) -> str or bool:
        """
        Метод для создания пути для файла, если путь не существует на диске,
        то будет создан
        @param user_id: int - id пользователя.
        @param order_id: int - id заказа.
        @param not_check: bool - проверка существования пути на YandexDisk, и
        его создание в случае отсутствия. По умолчанию False - проверка
        выполняется.
        @return:
        """
        path = os.path.join(self.dir_path, str(user_id), str(order_id))
        if not_check:
            return path

        if self._check_or_create(path):
            return path

    def _check_or_create(self, path: str) -> bool:
        """
        Метод проверяет существование указанной директории,
        и если её нет, то создает.
        @param path: Путь
        @return: bool
        """
        dirs = path.split("/")
        create_dirs = []
        for item in reversed(dirs):
            indx = dirs.index(item)
            path = str(os.path.join(*dirs[0 : indx + 1]))
            state = self._check_path(path)
            if not state:
                create_dirs.append(path)
            elif state:
                break

        for item in reversed(create_dirs):
            if not self._create_path(item):
                return False
        return True

    def _get_upload_link(self, path, order_id, name):
        """
        Метод для создания ссылки для загрузки.
        """
        full_path = f"{path}/{name}"
        params = {"path": full_path, "overwrite": self.overwrite}
        res = requests.get(
            f"{self.URL}/upload", headers=self.headers, params=params
        )
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
        result["status_code"] = response.status_code
        if response.status_code == 201:
            result["yandex_path"] = path + "/" + name

        return result

    def cloud_get_file(self, yandex_path):
        """
        Метод для получения файла из YandexDisk.
        """

        res = requests.get(
            f"{self.URL}/download/?path={yandex_path}", headers=self.headers
        )
        download_url = res.json().get("href")

        if not download_url:
            raise FileNotFound()

        result = {"status": res.status_code, "download_url": download_url}
        return result

    def cloud_delete_file(self, yandex_path):
        """Метод для удаления файла из YandexDisk."""
        res = requests.delete(
            f"{self.URL}?path={yandex_path}&permanently=True",
            headers=self.headers,
        )
        # если файл на сервере удален или не найден возвращаем True
        if res.status_code not in [202, 204, 404]:
            raise errorcode.IncorrectFileDeleting
        return True

    def cloud_copy_files(
        self, path_from: str, path_to: str, overwrite=False
    ) -> bool or str:
        """
        Метод копирует файлы расположенные на YandexDisk.
        Пути должны существовать.
        @param path_from: str - Путь до файла/директории которые
        копируем.
        @param path_to: str - Путь до директории/файла в которые
        копируем.
        @param overwrite: bool - признак перезаписи, по умолчанию False
        @return: bool or dict - Статус выполнения: True - успех,
        str - в процессе (возвращается id операции), False - неуспешно.
        """

        data = {"from": path_to, "path": path_from, "overwrite": overwrite}
        res = requests.post(
            url=f"{self.URL}/copy", params=data, headers=self.headers
        )
        if res.status_code == 201:
            return True
        elif res.status_code == 202:
            return res.json().get("href")
        return errorcode.CopyingFileError

    def create_order_path(
        self, user_id: int or str, order_id: int, not_check=False
    ) -> str:
        """
        Метод возвращает путь до директории с файлами заказа
        @param user_id: int - id пользователя
        @param order_id: int - id заказа
        @param not_check: bool - проверка существования пути на YandexDisk, и
        его создание в случае отсутствия. По умолчанию False - проверка
        выполняется.
        @return: str - путь до директории
        """
        return self._ensure_path_exists(user_id, order_id, not_check)

    def check_status_operation(self, operation_id: str) -> str:
        """
        Метод проверяет статус операции на YandexDisk
        @param operation_id: id операции
        @return: str - Статус операции (success, failed,
        """
        res = requests.get(url=operation_id, headers=self.headers)
        status = res.json().get("status")
        return status

    def cloud_move_files(
        self, path_from: str, path_to: str, overwrite=False
    ) -> bool or str:
        """
        Метод перемещает файлы расположенные на YandexDisk.
        @param path_from: str - Путь до файла/директории которые
        перемещаем.
        @param path_to: str - Путь до директории/файла в которые
        перемещаем.
        @param overwrite: bool - признак перезаписи, по умолчанию False
        @return: bool or dict - Статус выполнения: True - успех,
        str - в процессе (возвращается id операции), False - неуспешно.
        """

        data = {"from": path_to, "path": path_from, "overwrite": overwrite}
        res = requests.post(
            url=f"{self.URL}/move", params=data, headers=self.headers
        )
        if res.status_code == 201:
            return True
        elif res.status_code == 202:
            return res.json().get("href")
        return errorcode.CopyingFileError


class OffersCloudStorage(CloudStorage):
    """Класс для работы с файлами оффера на YandexCloud"""

    def __init__(self):
        super().__init__()
        self.dir_path = FILE_SETTINGS.get("PATH_OFFER_FILES")


class ChatsCloudStorage(CloudStorage):
    """Класс для работы с файлами чатов на YandexCloud"""

    def __init__(self):
        super().__init__()
        self.dir_path = FILE_SETTINGS.get("PATH_CHATS_FILES")
