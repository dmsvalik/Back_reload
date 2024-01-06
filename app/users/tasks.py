from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from app.sending.signals import new_notification

User = get_user_model()


@shared_task
def send_django_users_emails(email_class, context, user_id, recipients):
    """Отправка писем djoser через celery task."""
    if User.objects.filter(id=user_id).exists():
        email_class_object = import_string(email_class["type"])
        context.update({"user": User.objects.get(id=user_id)})
        email_class_object(context=context).send(recipients)
        new_notification.send(
            sender=None,
            user=context["user"],
            theme=email_class["theme"],
            type="email",
        )
