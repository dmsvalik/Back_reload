from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from app.sending.signals import new_notification

User = get_user_model()

logger = get_task_logger(__name__)


@shared_task()
def send_email_notification(sending, context, recipients):
    """Отправка писей пользователям."""
    try:
        notification_class = import_string(sending["type"])(context=context)
        notification_class.send(recipients)
        try:
            new_notification.send(
                sender=None,
                user=User.objects.get(id=context["user_id"]),
                theme=sending["theme"],
                type="email",
            )
        except Exception as er:
            logger.error(
                f"Ошибка при создании записи об отправке письма "
                f"пользователям с ошибкой {er}"
            )
    except Exception as er:
        logger.error(
            f"Ошибка при отправке письма пользователям {recipients} с "
            f"ошибкой {er}"
        )
