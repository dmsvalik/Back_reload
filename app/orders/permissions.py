from rest_framework import permissions

from app.orders.models import OrderFileData, OrderModel
from app.utils.errorcode import FileNotFound
from config.settings import ORDER_COOKIE_KEY_NAME


class IsOrderFileDataOwnerWithoutUser(permissions.BasePermission):
    """Проверка что пользователь является владельцем файла."""

    def has_permission(self, request, view):
        key = request.COOKIES.get(ORDER_COOKIE_KEY_NAME)
        file_id = request.data.get("file_id")
        if not OrderFileData.objects.filter(id=file_id).exists():
            raise FileNotFound()
        if OrderFileData.objects.filter(
            id=file_id, order_id__key=key, order_id__user_account__isnull=True
        ).exists():
            return True
        if (
            request.user.is_authenticated
            and OrderFileData.objects.filter(
                id=file_id, order_id__user_account=request.user
            ).exists()
        ):
            return True
        return False


class IsOrderOwner(permissions.BasePermission):
    """Проверка что пользователь является владельцем заказа."""

    def has_permission(self, request, view):
        key = request.COOKIES.get("key")
        order_id = view.kwargs.get("pk") or request.data.get("order_id")
        if OrderModel.objects.filter(
            id=order_id, key=key, user_account__isnull=True
        ).exists():
            return True
        if (
            request.user.is_authenticated
            and OrderModel.objects.filter(
                id=order_id, user_account=request.user
            ).exists()
        ):
            return True
        return False


class IsFileExistById(permissions.BasePermission):
    """Проверка на наличие информации о запрошенном файле в БД"""

    message = {"detail": "No file information found for the specified id"}

    def has_permission(self, request, view):
        file_id = (
            view.kwargs.get("file_id")
            if view.kwargs.get("file_id")
            else request.data.get("file_id")
        )

        return OrderModel.objects.filter(id=file_id).exists()
