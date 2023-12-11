from celery import shared_task

from app.sending import email_sending


@shared_task()
def send_email_notification(sending, context, recipients):
    notification_class = eval(sending)(context=context)
    notification_class.send(recipients)
