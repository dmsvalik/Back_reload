from app.sending.signals import new_notification
from app.sending.tasks import send_email_notification
from app.users.models import UserAccount

from config.settings import NOTIFICATION_CLASSES


def send_user_notifications(
    user: UserAccount, notification_class: str, context: dict, recipients: list
):
    """Отправка уведомлений пользователям и создание записи об отправке."""
    notifications_types = [
        notification.notification_type
        for notification in user.usernotifications_set.all()
    ]
    if "email" in notifications_types:
        send_email_notification.delay(
            NOTIFICATION_CLASSES["email"].get(notification_class)["type"],
            context,
            recipients,
        )
        new_notification.send(
            sender=None,
            user=user,
            theme=NOTIFICATION_CLASSES["email"].get(notification_class)[
                "theme"
            ],
            type="email",
        )

    if "tel" in notifications_types:
        pass
