import os
from app.file import exception as ex


class WorkFilePathMixin:
    """Набор методов для работы со строковым представлением пути файлов"""

    @staticmethod
    def generate_path(*args):
        """Метод генерирует строковый путь на основе переданных
        позиционных аргументов. Внимание: Важно передавать аргументы списком
        с аргументами расположенными в правильном порядке"""
        if len(args) <= 1:
            raise ex.FewElementsError
        path = os.path.join(*map(lambda x: str(x), args)).__str__()
        return path

    @staticmethod
    def get_file_format(filename: str) -> str:
        """Метод получает формат файла из любого пути"""
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def get_filename_from_path(path: str) -> str:
        """Метод получает имя файла из пути до него"""
        file_name = os.path.split(path)[1]
        if "." in file_name:
            return file_name
        else:
            raise ex.ThisNotFileError

    @staticmethod
    def replace_filename_from_path(path: str, filename: str) -> str:
        if "." not in path or "." not in filename:
            raise ex.ThisNotFileError

        dir_path = os.path.dirname(path)
        new_path = os.path.join(dir_path, filename).__str__()
        return new_path
