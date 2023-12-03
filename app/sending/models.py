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


class SentNotification(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата уведомления", auto_now_add=True)
    theme = models.CharField("Тема уведомления", max_length=200)
    type = models.CharField("Тип уведомления", max_length=200)

    class Meta:
        verbose_name = "Отправленное уведомление"
        verbose_name_plural = "Отправленные уведомления"
