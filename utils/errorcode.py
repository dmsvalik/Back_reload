from rest_framework.exceptions import APIException
from rest_framework import status


class HttpValidationException(APIException):
    """
        Шаблон для создания ошибок на базе ValidationError

    """

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error message"
    default_code = 'Invalid'

    def __init__(self, status_code=None):
        if status_code is not None:
            self.status_code = status_code


class IncorrectImageOrderUpload(HttpValidationException):
    status_code = 400
    detail = "Please check the order_id field it's incorrect"




