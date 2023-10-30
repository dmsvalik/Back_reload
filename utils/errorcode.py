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


class NotAllowedUser(HttpValidationException):
    status_code = 403
    detail = {"errors": "NotAllowedUser",
              "Description": "Доступ запрещен."}


class IncorrectPostParameters(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectPostParameters",
              "Description": "Пожалуйста, проверьете если заполнены все необходимые поля."}


class IncorrectImageOrderUpload(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectImageOrderUpload",
              "Description": "Указан неправильный id заказа."}


class IncorrectEmailCreateUser(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectEmailCreateUser",
              "Description": "Допускаются англиский буквы, числа, точки, знаки: '-' и '@'. "
                             "Длинна почты не менее 5 и не более 50 знаков. "}


class IncorrectSurnameCreateUser(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectSurnameCreateUser",
              "message": "Допускаются только английские и русские буквы. Длинна фамилии не менее 2 букв и не более 20."}


class IncorrectNameCreateUser(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectNameCreateUser",
              "message": "Допускаются только английские и русские буквы. Длинна имени не менее 2 букв и не более 20."}


class IncorrectTelephoneCreateUser(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectTelephoneCreateUser",
              "message": "Номер телефона должен начинаться на +7 и иметь 12 цифровых символов."}


class IncorrectPasswordCreateUser(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectPasswordCreateUser",
              "message": "Длинна пароля не менее 8 и не более 64 знаков, английский алфавит, использование не менне 1 цифры."
                         "Разрешены следующие символы: ~ ! ? @ # $ % ^ & * _ - + ( ) [ ] { } > < / \ | ' . , :"}


class IncorrectImageDeleting(HttpValidationException):
    status_code = 400
    detail = {"errors": "IncorrectImageDeleting",
              "message": "Возникла ошибка при удалении изображения."}


class OrderIdNotFound(HttpValidationException):
    status_code = 404
    detail = {"errors": "OrderIdNotFound",
              "message": "Заказ не найдет."}


class UniqueOrderOffer(HttpValidationException):
    status_code = 403
    detail = {"errors": "UniqueOrderOffer",
              "message": "Вы можете создать только одно предложение на каждый заказ."}


class NotContractorOffer(HttpValidationException):
    status_code = 403
    detail = {"errors": "NotContractorOffer",
              "message": "Только исполнитель может создать предложение к заказу."}


class ContractorIsInactive(HttpValidationException):
    status_code = 403
    detail = {"errors": "ContractorIsInactive",
              "message": "Исполнитель не активен."}


class OrderInWrongStatus(HttpValidationException):
    status_code = 403
    detail = {"errors": "OrderInWrongStatus",
              "message": "Статус заказа не позволяет сейчас сделать предложение."}


class DocumentPermission(HttpValidationException):
    status_code = 403
    detail = {"errors": "DocumentPermission",
              "message": "У Вас нет доступа к этому файлу."}


class FileNotFound(HttpValidationException):
    status_code = 404
    detail = {"errors": "FileNotFound",
              "message": "Файл не найден."}


class CategoryIdNotFound(HttpValidationException):
    status_code = 404
    detail = {"errors": "CategoryIdNotFound",
              "message": "Категория не найдена."}
