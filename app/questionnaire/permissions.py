from rest_framework import permissions

from app.orders.models import OrderModel


class IsOrderOwnerWithoutUser(permissions.BasePermission):
    def has_permission(self, request, view):
        key = request.COOKIES.get("key")
        if OrderModel.objects.filter(
            key=key, user_account__isnull=True
        ).exists():
            return True
        return False
