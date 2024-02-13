import os
import random
import string

from config.settings import BASE_DIR, FILE_SETTINGS


class ServerFileBase:
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
                self._generate_path(self._server_dir, path)
            )

    @staticmethod
    def _generate_path(*args):
        """Метод генерирует строковый путь на основе переданных
        позиционных аргументов. Внимание: Важно передавать аргументы списком
        с аргументами расположенными в правильном порядке"""
        path = os.path.join(*args).__str__()
        return path

    @staticmethod
    def _check_or_create(path: str) -> str:
        """Метод проверяет наличие заданной директории, если директория
        не найдена - создает"""
        if not os.path.exists(path):
            os.makedirs(path)
        return path

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

    @staticmethod
    def get_file_format(filename: str) -> str:
        """Метод получает формат файла из его имени"""
        return filename.split(".")[-1]

    def get_unique_filename(self, old_name: str) -> str:
        """Метод генерирует уникальное имя файла на основе директории
        предполагаемого сохранения файла"""
        existed_names = os.listdir(self._server_dir)
        new_name = self._get_random_filename()
        while new_name in existed_names:
            new_name = self._get_random_filename()

        return f"{new_name}.{self.get_file_format(old_name)}"

    def save(self, path: str, file) -> str:
        """Метод сохраняет файл в указанную директорию"""
        path_to_save = os.path.join(self._server_dir, path).__str__()
        with open(path_to_save, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return path_to_save


class TmpServerFiles(ServerFileBase):
    def __init__(self, path: str = "tmp"):
        super().__init__(path)
