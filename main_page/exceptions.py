from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class EmailTimestampError(PermissionDenied):
    """ Проверка отправки почты по смене почты - запрет на 3 часа """

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'We already have send message to this email. Try letter.'
    default_code = 'permission_denied'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
