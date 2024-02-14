class ThisNotFileError(Exception):
    def __init__(self):
        self.message = "Данный путь не содержит имени конечного файла"

    def __str__(self):
        return self.message
