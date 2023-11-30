from django.db.models.signals import post_save

from app.users.models import UserAccount
from app.sending.models import UserNotifications


def create_user_notification(sender, instance, created, **kwargs):
    if created:
        UserNotifications.objects.create(user=instance)


post_save.connect(create_user_notification, sender=UserAccount)
