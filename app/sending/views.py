
from app.sending.signals import new_notification
from app.sending.tasks import send_email_notification
from app.users.models import UserAccount


NOTIFICATION_CLASSES = {
    "email": {
        "ORDER_CREATE_CONFIRMATION": {
            "type": "app.sending.email_sending.OrderEmail",
            "theme": "Подтверждение отправки заказа исполнителям."
        }
    },
    "tel": {
        "ORDER_CREATE_CONFIRMATION": None
    }
}


def send_user_notifications(user: UserAccount, notification_class: str, context: dict, recipients: list):
    notifications_types = [notification.notification_type for notification in user.usernotifications_set.all()]
    if "email" in notifications_types:
        send_email_notification.delay(
            NOTIFICATION_CLASSES["email"].get(notification_class)["type"],
            context,
            recipients)
        new_notification.send(sender=None, user=user,
                              theme=NOTIFICATION_CLASSES["email"].get(notification_class)["theme"],
                              type="email")

    if "tel" in notifications_types:
        pass
