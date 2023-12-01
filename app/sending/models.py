from django.db import models

from app.users.models import UserAccount


class UserNotifications(models.Model):
    class NotificationTypes(models.TextChoices):
        NONE = None, "Уведомления отключены"
        EMAIL = "email", "Уведомление по Email"
        TEL = "tel", "Уведомление по номеру телефона"

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null=False)
    notification_type = models.CharField(choices=NotificationTypes.choices, max_length=10,
                                         null=True, blank=False, default=None)

    class Meta:
        verbose_name = "Тип уведомлений"
        verbose_name_plural = "Типы уведомлений"
