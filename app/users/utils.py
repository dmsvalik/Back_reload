from django.db.models import Sum, QuerySet, F, Sum

from app.orders.models import OrderFileData, FileData
from app.users.models import UserAccount, UserQuota


class UserQuotaManager:

    def __init__(self, user: UserAccount):
        self.user = user


    def add(self, file: OrderFileData | FileData) -> UserQuota:
        """
        Добавляет размеры переданного файла к квоте юзер
        """
        user_quota: UserQuota = UserAccount.objects.get_or_create(user=self.user)[0]
        (
            UserQuota.objects.
            filter(pk=user_quota.pk)
            .update(
                total_cloud_size=F("total_cloud_size")+file.yandex_size,
                total_server_size=F("total_server_size")+file.server_size
                )
            )
        return user_quota


    def add_many(self, files: QuerySet[OrderFileData | FileData]) -> UserQuota:
        """
        Добавляет сумму переданных файлов к квоте
        """
        user_quota: UserQuota = UserQuota.objects.get_or_create(user=self.user)[0]
        (
            UserQuota.objects
            .filter(pk=user_quota.pk)
            .update(
                total_cloud_size=F("total_cloud_size")+files.aggregate(cloud_size=Sum("yandex_size")).get("cloud_size"),
                total_server_size=F("total_server_size")+files.aggregate(server_size=Sum("server_size")).get("server_size")
                )
            )
        return user_quota


    def subtract(self, file: OrderFileData | FileData) -> UserQuota:
        """
        Вычитает размеры переданного файла из квоты юзера
        """
        user_quota: UserQuota = UserAccount.objects.get_or_create(user=self.user)[0]
        (
            UserQuota.objects
            .filter(pk=user_quota.pk)
            .update(
                total_cloud_size=F("total_cloud_size")-file.yandex_size,
                total_server_size=F("total_server_size")-file.server_size
                )
            )
        return user_quota

    def subtract_many(self, files: QuerySet[OrderFileData | FileData]) -> UserQuota:
        """
        Вычитает сумму переданных фалов из квоты
        """
        user_quota: UserQuota = UserAccount.objects.get_or_create(user=self.user)[0]
        (
            UserQuota.objects
            .filter(pk=user_quota.pk)
            .update(
                total_cloud_size=F("total_cloud_size")+files.aggregate(cloud_size=Sum("yandex_size")).get("cloud_size"),
                total_server_size=F("total_server_size")+files.aggregate(server_size=Sum("server_size")).get("server_size")
                )
            )

        return user_quota


    def quota(self) -> UserQuota:
        """
        Возвращает текущую квоту юзера
        """
        return UserQuota.objects.filter(user=self.user)
