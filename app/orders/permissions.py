from django.db.models import Sum
from rest_framework import permissions

from app.utils.errorcode import (
    FileNotFound,
    UniqueOrderOffer,
)
from app.orders.models import OrderFileData, OrderModel, OrderOffer
from app.users.utils.quota_manager import UserQuotaManager
from config.settings import (
    ORDER_COOKIE_KEY_NAME,
    MAX_SERVER_QUOTA,
    MAX_STORAGE_QUOTA,
)


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

    message = {"detail": "You are not the order owner"}

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


class OneOfferPerContactor(permissions.BasePermission):
    """
    Ограничение на создание нескольких предложений
    к одному заказу от 1 исполнителя
    """

    def has_permission(self, request, view):
        user = request.user
        order_id = view.kwargs.get("pk")

        if OrderOffer.objects.filter(
            user_account=user, order_id=order_id
        ).exists():
            raise UniqueOrderOffer()
        return True


class IsOrderExists(permissions.BasePermission):
    """Проверка на наличие заказа"""

    message = {"detail": "No order information found for the specified id"}

    def has_permission(self, request, view):
        order_id = view.request.data.get("order_id")
        return OrderModel.objects.filter(id=order_id).exists()


class IsUserQuotaForClone(permissions.BasePermission):
    """Проверка на наличие места для копирования всех файлов заказа"""

    message = {"detail": "There is not enough space to copy order files"}

    def has_permission(self, request, view):
        order_id = view.request.data.get("order_id")
        files = OrderFileData.objects.filter(order_id=order_id)
        user = OrderModel.objects.get(pk=order_id).user_account

        quota_manager = UserQuotaManager(user)
        quota = quota_manager.quota()

        proj_yandex_size = (
            files.aggregate(cloud_size=Sum("yandex_size")).get("cloud_size")
            + quota.total_cloud_size
        )
        proj_server_size = (
            files.aggregate(server_size=Sum("server_size")).get("server_size")
            + quota.total_server_size
        )

        return (
            proj_server_size < MAX_SERVER_QUOTA
            and proj_yandex_size < MAX_STORAGE_QUOTA
        )
