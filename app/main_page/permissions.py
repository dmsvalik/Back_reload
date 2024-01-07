from rest_framework import permissions, serializers

from app.main_page.models import ContractorData


class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь исполнителем.
        Использовать только после IsAuthenticated
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not (
            request.user.is_staff
            or ContractorData.objects.filter(user_id=request.user.id).exists()
        ):
            raise serializers.ValidationError("Вы не являетесь исполнителем")
        return True
