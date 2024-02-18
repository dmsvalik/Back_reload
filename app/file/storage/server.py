import os
import random
import shutil
import string

from PIL import Image

from .mixin import WorkFilePathMixin
from config.settings import BASE_DIR, FILE_SETTINGS


class ServerFileBase(WorkFilePathMixin):
    _server_dir = os.path.join(
        BASE_DIR, FILE_SETTINGS.get("PATH_SERVER_FILES")
    ).__str__()
    NUMBER_OF_CHARACTERS_IN_FILENAME = FILE_SETTINGS.get(
        "NUMBER_OF_CHARACTERS_IN_FILENAME"
    )

    def __init__(self, path: str = None):
        if path is None:
            self.path = self._server_dir
        else:
            self.path = self._check_or_create(
                self.generate_path(self._server_dir, path)
            )

    @staticmethod
    def _check_or_create(path: str) -> str:
        """Метод проверяет наличие заданной директории, если директория
        не найдена - создает"""
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def generate_abspath(self, path: str) -> str:
        return self.generate_path(self._server_dir, path)

    def check_path(self, path: str) -> bool:
        abs_path = self.generate_abspath(path)
        if os.path.exists(abs_path):
            return True
        return False

    def _get_filename_list(self):
        """Метод получает список имен файлов указанной директории"""
        filename_lst = []
        for path in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, path)):
                filename = path.split(".")[0]
                filename_lst.append(filename)
        return filename_lst

    def _get_random_filename(self):
        """Метод генерирует строку заданной в настройках длины имени файла"""
        file_name = "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=self.NUMBER_OF_CHARACTERS_IN_FILENAME,
            )
        )
        return file_name

    def get_unique_filename(self, old_name: str) -> str:
        """Метод генерирует уникальное имя файла на основе директории
        предполагаемого сохранения файла"""
        existed_names = self._get_filename_list()
        new_name = self._get_random_filename()
        while new_name in existed_names:
            new_name = self._get_random_filename()

        return f"{new_name}.{self.get_file_format(old_name)}"

    def get_size(self, path):
        abs_path = self.generate_abspath(path)
        return os.path.getsize(abs_path)

    def save(self, path: str, file) -> tuple[str, int]:
        """Метод сохраняет файл в указанную директорию"""
        path_to_save = self.generate_abspath(path)
        with open(path_to_save, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        size = self.get_size(path)
        return path, size

    def delete(self, path: str) -> None:
        """Метод удаляет файл по заданному пути"""
        abs_path = self.generate_abspath(path)
        os.remove(abs_path)

    def moving_file(self, old_path: str, new_path: str) -> str:
        abs_dir_path = self.generate_abspath(new_path)
        self._check_or_create(abs_dir_path)

        filename = self.get_filename_from_path(old_path)
        abs_path = os.path.join(abs_dir_path, filename)
        shutil.move(old_path, abs_path)

        return self.generate_path(new_path, filename)


class ServerImageFiles(ServerFileBase):
    """Класс для работы с изображениями"""

    MAXIMUM_DIMENSIONS_OF_SIDES = FILE_SETTINGS.get(
        "MAXIMUM_DIMENSIONS_OF_SIDES"
    )
    MAX_IMAGE_SIZE_IN_B = FILE_SETTINGS["MAX_IMAGE_SIZE_IN_B"]
    COEFFICIENT_OF_SIZE_CHANGING = FILE_SETTINGS[
        "IMAGE_COEFFICIENT_OF_SIZE_CHANGING"
    ]

    def __init__(self, path: str = None):
        super().__init__(path)

    def save_preview(self, path: str):
        abs_path = self.generate_abspath(path)
        filename = self.get_filename_from_path(path)
        new_filename = self.get_unique_filename(filename)
        preview_path = self.replace_filename_from_path(abs_path, new_filename)

        img = Image.open(abs_path)
        img.thumbnail(self.MAXIMUM_DIMENSIONS_OF_SIDES)
        img.save(preview_path)

        size = self.get_size(preview_path)
        preview_path = self.replace_filename_from_path(path, new_filename)

        return preview_path, size

    def _image_compression(self, path: str):
        """Сжатие изображения согласно коэффициента заданного в настройках"""
        image_size = os.path.getsize(path)
        if image_size > self.MAX_IMAGE_SIZE_IN_B:
            img = Image.open(path)
            while image_size > self.MAX_IMAGE_SIZE_IN_B:
                img = img.resize(
                    (
                        int(img.size[0] * self.COEFFICIENT_OF_SIZE_CHANGING),
                        int(img.size[1] * self.COEFFICIENT_OF_SIZE_CHANGING),
                    )
                )
                img.save(path)
                image_size = os.path.getsize(path)
        return image_size

    def save(self, path: str, file) -> tuple[str, int]:
        """Метод сохраняет файл в указанную директорию"""
        path_to_save, size = super().save(path, file)
        filename = self.get_filename_from_path(path)
        abs_path = self.generate_path(self.path, filename)
        size = self._image_compression(abs_path)
        return path_to_save, size


class ServerFiles(ServerFileBase):
    def __init__(self, path: str = None):
        super().__init__(path)
