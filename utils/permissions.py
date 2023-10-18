from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from orders.models import FileData
from utils import errorcode


class IsContactorOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        path = view.kwargs['path']
        file_exists = FileData.objects.filter(server_path__contains=path, user_account=request.user).exists()
        if not request.user.role == 'contractor' or file_exists:
            raise errorcode.DocumentPermission()
        return True
