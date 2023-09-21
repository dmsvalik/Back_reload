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


class IncorrectEmailCreateUser(HttpValidationException):
    status_code = 400
    detail = "English letters, numbers, dashes, dots, @. Length is not less than 5 and not more than 50 characters."


class IncorrectSurnameCreateUser(HttpValidationException):
    status_code = 400
    detail = "English or Russian letters. Length is not less than 2 and not more than 50 characters."


class IncorrectTelephoneCreateUser(HttpValidationException):
    status_code = 400
    detail = "The phone number must start with +7 and have 12 characters (digits)."


class IncorrectPasswordCreateUser(HttpValidationException):
    status_code = 400
    detail = "Length from 8 to 20 characters, english alphabet, number, symbols. " \
             "including at least one numeric and one non-alphanumeric character"