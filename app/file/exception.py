class ThisNotFileError(Exception):
    def __init__(self):
        self.message = "Данный путь не содержит имени конечного файла"

    def __str__(self):
        return self.message


class FewElementsError(Exception):
    def __init__(self):
        self.message = "Недостаточно элементов для генерации пути"

    def __str__(self):
        return self.message


class CloudError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
