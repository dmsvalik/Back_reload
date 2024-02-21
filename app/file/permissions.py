from rest_framework import permissions

from app.file.models import FileModel
from app.file.utils.helpers import get_client_ip
from app.users.models import UserQuota
from app.utils.errorcode import IpFileUploadLimit
from config.settings import IP_LIMIT_B, MAX_STORAGE_QUOTA, MAX_SERVER_QUOTA


class IpFileSizeLimit(permissions.BasePermission):
    """Проверка что статус заказа позволяет принимать офферы."""

    def has_permission(self, request, view):
        ip = get_client_ip(request)
        if (
            sum(
                FileModel.objects.prefetch_related("ipfilemodel")
                .filter(ipfilemodel__ip=ip)
                .values_list("server_size", flat=True)
            )
            > IP_LIMIT_B
        ):
            raise IpFileUploadLimit()
        return True


class UserQuotaLimit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            quota: UserQuota = request.user.userquota
            if (
                quota.total_cloud_size > MAX_STORAGE_QUOTA
                or quota.total_server_size > MAX_SERVER_QUOTA
            ):
                raise IpFileUploadLimit()
        return True
