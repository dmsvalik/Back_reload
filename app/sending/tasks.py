from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.module_loading import import_string

logger = get_task_logger(__name__)


@shared_task()
def send_email_notification(sending, context, recipients):
    try:
        notification_class = import_string(sending)(context=context)
        notification_class.send(recipients)
    except Exception as er:
        logger.error(
            f"Ошибка при отправке письма пользователям {recipients} с ошибкой {er}"
        )
