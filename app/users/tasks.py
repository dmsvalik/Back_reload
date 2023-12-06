from celery import shared_task

from app.users.models import UserAccount


@shared_task
def send_django_users_emails(request, email_class, user_id, recipients):
    if UserAccount.objects.filter(id=user_id).exists():
        context = {"user": UserAccount.objects.get(id=user_id)}
        email_class(request, context).send(recipients)
