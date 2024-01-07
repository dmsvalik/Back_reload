from rest_framework import permissions

from app.orders.models import OrderModel
from config.settings import ORDER_COOKIE_KEY_NAME


class IsOrderOwnerWithoutUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Проверяет, является ли неавторизованный пользователь создателем заказа.
        Проверяет на наличие ключа в cookies.
        """
        key = request.COOKIES.get(ORDER_COOKIE_KEY_NAME)
        if OrderModel.objects.filter(
            key=key, user_account__isnull=True
        ).exists():
            return True
        return False
