from django.db.models import Q
from rest_framework import permissions

from app.orders.models import OrderFileData
from app.utils import errorcode


class IsContactor(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if current user is "contractor" and is authenticated
        """
        if request.user.is_authenticated and request.user.role == 'contractor':
            return True
        return False


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
        """
        Returns True if the file "server path" field
        contains path from the URL
        and the file is created by the current user
        """
        path = view.kwargs['path']
        current_user = request.user
        file = (
            OrderFileData.objects
            .filter(
                Q(server_path__contains=path) & Q(order_id__user_account=current_user)
            )
            .first()
            )
        if not file:
            return False
        return True
