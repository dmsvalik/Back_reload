from django.db.models import Sum, QuerySet, F

from app.orders.models import OrderFileData, FileData
from app.users.models import UserAccount, UserQuota


class UserQuotaManager:
    def __init__(self, user: UserAccount):
        self.user: UserAccount = user
        self.user_quota: UserQuota = UserQuota.objects.filter(
            user=self.user
        ).first()

    def add(
        self,
        file: OrderFileData | FileData,
        server: bool = True,
        cloud: bool = True,
    ) -> UserQuota:
        """
        Добавляет размеры переданного файла к квоте юзер
        """
        update_fields: dict = {}
        if server:
            update_fields["total_server_size"] = (
                F("total_server_size") + file.server_size
            )
        if cloud:
            update_fields["total_cloud_size"] = (
                F("total_cloud_size") + file.yandex_size
            )
        (
            UserQuota.objects.filter(pk=self.user_quota.pk).update(
                **update_fields
            )
        )
        return self.user_quota

    def add_many(
        self,
        files: QuerySet[OrderFileData | FileData],
        server: bool = True,
        cloud: bool = True,
    ) -> UserQuota:
        """
        Добавляет сумму переданных файлов к квоте
        """
        sizes: dict = files.aggregate(
            cloud_size=Sum("yandex_size"), server_size=Sum("server_size")
        )
        update_fields: dict = {}
        if cloud:
            update_fields["total_cloud_size"] = F(
                "total_cloud_size"
            ) + sizes.get("cloud_size")
        if server:
            update_fields["total_server_size"] = F(
                "total_server_size"
            ) + sizes.get("server_size")

        (
            UserQuota.objects.filter(pk=self.user_quota.pk).update(
                **update_fields
            )
        )

        return self.user_quota

    def subtract(self, file: OrderFileData | FileData) -> UserQuota:
        """
        Вычитает размеры переданного файла из квоты юзера
        """
        (
            UserQuota.objects.filter(pk=self.user_quota.pk).update(
                total_cloud_size=F("total_cloud_size") - file.yandex_size,
                total_server_size=F("total_server_size") - file.server_size,
            )
        )
        return self.user_quota

    def subtract_many(
        self, files: QuerySet[OrderFileData | FileData]
    ) -> UserQuota:
        """
        Вычитает сумму переданных фалов из квоты
        """
        sizes: dict = files.aggregate(
            cloud_size=Sum("yandex_size"), server_size=Sum("server_size")
        )
        (
            UserQuota.objects.filter(pk=self.user_quota.pk).update(
                total_cloud_size=F("total_cloud_size")
                + sizes.get("cloud_size"),
                total_server_size=F("total_server_size")
                + sizes.get("server_size"),
            )
        )

        return self.user_quota

    def quota(self) -> UserQuota:
        """
        Возвращает текущую квоту юзера
        """
        return UserQuota.objects.filter(user=self.user).first()
