from datetime import datetime, timedelta

from rest_framework import permissions
from rest_framework.exceptions import ValidationError


from app.orders.models import OrderFileData, OrderModel
from app.utils.errorcode import FileNotFound



class ChangePriceInOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.data.get("offer_price") and request.method in "POST":
            raise ValidationError(
                "Цену можно указать только через день после размещения заказа"
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.data.get("offer_price"):
            if request.method in ("PATH", "PUT"):
                if datetime.now().replace(tzinfo=None) < obj.offer_create_at.replace(
                    tzinfo=None
                ) + timedelta(days=1):
                    raise ValidationError(
                        "Цену можно указать только через день после размещения заказа"
                    )
        return True


class IsOrderFileDataOwnerWithoutUser(permissions.BasePermission):
    def has_permission(self, request, view):
        key = request.COOKIES.get('key')
        file_id = request.data.get('file_id')
        if not OrderFileData.objects.filter(id=file_id).exists():
            raise FileNotFound()
        if OrderFileData.objects.filter(id=file_id, order_id__key=key, order_id__user_account__isnull=True).exists():
            return True
        if request.user.is_authenticated and OrderFileData.objects.filter(
                id=file_id,
                order_id__user_account=request.user
        ).exists():
            return True
        return False

      
class IsOrderOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        key = request.COOKIES.get('key')
        order_id = view.kwargs.get('pk')
        if OrderModel.objects.filter(id=order_id, key=key, user_account__isnull=True).exists():
            return True
        if request.user.is_authenticated and OrderModel.objects.filter(id=order_id, user_account=request.user).exists():
            return True
        return False
