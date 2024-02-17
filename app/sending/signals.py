from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal

from app.sending.models import UserNotifications, SentNotification
from app.users.models import UserAccount

# Запись в бд об отправке уведомления.
# Args: user: UserAccount, theme: "string", type: "string"
new_notification = Signal()


def create_user_notification(sender, instance, created, **kwargs):
    """
    Создание объекта уведомления пользователя по email
    при создании пользователя.
    """
    if created:
        UserNotifications.objects.create(user=instance)


post_save.connect(create_user_notification, sender=UserAccount)


def create_notification_record(
    sender, user: UserAccount, theme: str, type: str, **kwargs
):
    """Создание записи об уведомлении пользователя."""
    SentNotification.objects.create(user=user, theme=theme, type=type)


new_notification.connect(create_notification_record)


def update_if_user_no_notifications(sender, instance, **kwargs):
    """
    Обновление поля уведомлений пользователя.
    При отключении всех уведомлений.
    """
    user = UserAccount.objects.get(id=instance.user.id)
    if not user.usernotifications_set.all():
        user.notifications = False
        user.save()


post_delete.connect(update_if_user_no_notifications, sender=UserNotifications)


def update_if_user_has_notifications(sender, instance, created, **kwargs):
    """
    Обновление поля уведомлений пользователя.
    При создании типа уведомлений.
    """
    user = UserAccount.objects.get(id=instance.user.id)
    if not user.notifications:
        user.notifications = True
        user.save()


post_save.connect(update_if_user_has_notifications, sender=UserNotifications)
