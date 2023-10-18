from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from orders.models import FileData
from utils import errorcode


class IsContactor(permissions.BasePermission):
    def has_permission(self, request, view):
        path = view.kwargs['path']
        file = FileData.objects.get(server_path__contains=path)
        if not request.user.role == 'contractor':
            return False
        return True


class IsFileExist(permissions.BasePermission):
    def has_permission(self, request, view):
        path = view.kwargs['path']
        file_exists = FileData.objects.filter(server_path__contains=path).exists()
        if file_exists:
            return True
        raise errorcode.FileNotFound()


class IsFileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        path = view.kwargs['path']
        file = FileData.objects.get(server_path__contains=path)
        if not file.user_account == request.user:
            return False
        return True
