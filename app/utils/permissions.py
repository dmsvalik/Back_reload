from django.db.models import Q
from rest_framework import permissions

from app.orders.models import OrderFileData
from app.utils import errorcode


class IsContactor(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if current user is "contractor"
        """
        current_user = request.user

        if not current_user.role == 'contractor':
            return False
        return True


class IsFileExist(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if the file is exists
        """
        path = view.kwargs['path']
        file_exists = OrderFileData.objects.filter(server_path__contains=path).exists()

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
