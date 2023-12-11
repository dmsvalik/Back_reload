from celery import shared_task
from django.utils.module_loading import import_string


@shared_task()
def send_email_notification(sending, context, recipients):
    notification_class = import_string(sending)(context=context)
    notification_class.send(recipients)
