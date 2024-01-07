from django.contrib.auth import get_user_model

from app.sending.tasks import send_email_notification

from config.settings import NOTIFICATION_CLASSES

User = get_user_model()


def send_user_notifications(
    user: User, notification_class: str, context: dict, recipients: list
):
    """Отправка уведомлений пользователям и создание записи об отправке."""
    notifications_types = [
        notification.notification_type
        for notification in user.usernotifications_set.all()
    ]
    if "email" in notifications_types:
        send_email_notification.delay(
            NOTIFICATION_CLASSES["email"].get(notification_class),
            context,
            recipients,
        )

    if "tel" in notifications_types:
        pass
