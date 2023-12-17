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
        Returns True if:
        user is authenticated and the file "server path" field
        contains path from the URL
        and the file is created by the user
        OR
        Return True if: user is not authenticated and
        the file "server path" field
        contains path from the URL and
        key "key" from cookies is exists in the order
        """
        path = view.kwargs.get('path')
        file_id = request.data.get('file_id')
        filter_file = Q(server_path__contains=path) if path else Q(pk=file_id)
        current_user = request.user

        if current_user.is_authenticated:
            # search order owner
            filter_query = Q(order_id__user_account=current_user)
        else:
            # search order cookie key
            cookie_key = request.COOKIES.get("key")
            filter_query = Q(
                order_id__key=cookie_key) & Q(
                order_id__user_account__isnull=True)

        file = (
            OrderFileData.objects
            .filter(
                filter_file & filter_query
            )
            .first()
            )

        if not file:
            return False
        return True
