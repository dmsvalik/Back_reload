from django.db.models.signals import post_save
from django.dispatch import Signal

from app.sending.models import UserNotifications, SentNotification
from app.users.models import UserAccount

# Запись в бд об отправке уведомления. Args: user: UserAccount, theme: "string", type: "string"
new_notification = Signal()



def create_user_notification(sender, instance, created, **kwargs):
    if created:
        UserNotifications.objects.create(user=instance)


post_save.connect(create_user_notification, sender=UserAccount)


def create_notification_record(sender, user: UserAccount, theme: str, type: str, **kwargs):
    SentNotification.objects.create(
        user=user,
        theme=theme,
        type=type
    )


new_notification.connect(create_notification_record)
