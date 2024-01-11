import os
from functools import wraps

import magic
from django.http import HttpResponse

from app.orders.models import OrderModel
from app.users.models import UserQuota
from config.settings import (
    ALLOWED_TYPES_EXTENSIONS,
    MAX_ORDERS,
    MAX_SERVER_QUOTA,
    MAX_STORAGE_QUOTA,
)
from .constants import ErrorMessages


def check_user_quota(func):
    """Проверка доступной квоты пользователя."""

    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        user_id = request.user.id
        try:
            user_quota = UserQuota.objects.get(user_id=user_id)
        except UserQuota.DoesNotExist:
            return HttpResponse(ErrorMessages.USER_NOT_FOUNDED, status=404)

        if user_quota.total_cloud_size >= MAX_STORAGE_QUOTA:
            return HttpResponse(
                ErrorMessages.MAX_QUOTA_ERROR,
                status=403,
            )

        if user_quota.total_server_size >= MAX_SERVER_QUOTA:
            return HttpResponse(
                ErrorMessages.MAX_QUOTA_ERROR,
                status=403,
            )

        if user_quota.total_traffic < 0:
            return HttpResponse(
                ErrorMessages.TOTAL_TRAFFIC_ERROR,
                status=403,
            )

        return func(request, *args, **kwargs)

    return wrapped


def check_file_type(allowed_mime_types):
    """Проверка соответствия типов файлов допустимым."""

    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            uploaded_file = request.FILES.get("upload_file")
            if "upload_file" not in request.FILES:
                return HttpResponse(
                    ErrorMessages.UPLOADED_FILE_FIELD_ERROR,
                    status=400,
                )

            # Detect the file's MIME type
            file_type = magic.from_buffer(uploaded_file.read(1024), mime=True)

            # Check the MIME type against the list of allowed types
            if file_type not in allowed_mime_types:
                return HttpResponse(
                    ErrorMessages.UNSUPPORTED_FILE.format(f"{file_type}"),
                    status=400,
                )

            # Check the file extension is not the expected one
            extension = os.path.splitext(uploaded_file.name)[1]
            if extension.lower() not in ALLOWED_TYPES_EXTENSIONS[file_type]:
                return HttpResponse(
                    ErrorMessages.UNSUPPORTED_FILE.format(f"{file_type}"),
                    status=400,
                )

            return func(request, *args, **kwargs)

        return wrapped

    return decorator


def check_order_limit(func):
    """Проверка максимального количества заказов у пользователя."""

    @wraps(func)
    def wrapped(request, *args, **kwargs):
        user_id = request.user.id
        user_order_count = OrderModel.objects.filter(
            user_id=user_id, offer_status=False
        ).count()
        if user_order_count >= MAX_ORDERS:
            return HttpResponse(
                ErrorMessages.ORDER_LIMIT_ERROR.format(MAX_ORDERS),
                status=403,
            )

        return func(request, *args, **kwargs)

    return wrapped
