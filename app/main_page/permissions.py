from rest_framework import permissions, serializers

from app.main_page.models import ContractorData
from app.utils.errorcode import ContractorIsInactive


class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь исполнителем.
        Использовать только после IsAuthenticated
        """
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if not (
            request.user.is_staff
            or ContractorData.objects.filter(user_id=request.user.id).exists()
        ):
            raise serializers.ValidationError("Вы не являетесь исполнителем")
        return True


class IsActiveContactor(permissions.BasePermission):
    """
    Является ли исполнитель активным,
    пропускает юзера с правами staff
    """

    def has_permission(self, request, view):
        user = request.user
        contactor = ContractorData.objects.filter(user=user).first()
        if not user.is_staff:
            if not contactor and not contactor.is_active:
                raise ContractorIsInactive()
        return True
