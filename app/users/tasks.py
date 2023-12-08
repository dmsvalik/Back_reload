from celery import shared_task
from djoser.conf import settings as djoser_settings

from app.users.models import UserAccount


@shared_task
def send_django_users_emails(email_class, context, user_id, recipients):
    if UserAccount.objects.filter(id=user_id).exists():
        email_class = eval("djoser_settings" + "." + email_class)
        context.update({"user": UserAccount.objects.get(id=user_id)})
        email_class(context=context).send(recipients)
