from rest_framework import permissions

from app.file.models import FileModel
from app.file.utils.helpers import get_client_ip
from app.utils.errorcode import IpFileUploadLimit
from config.settings import IP_LIMIT_B


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
