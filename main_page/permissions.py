from rest_framework import permissions, serializers
from main_page.models import SellerData


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not (request.user.is_staff or SellerData.objects.get(id=request.user.id)):
            raise serializers.ValidationError("Вы не являетесь продавцом")
        return True
