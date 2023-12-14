from django.apps import AppConfig


class SendingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.sending"
    label = "sending"

    def ready(self):
        from app.sending.signals import create_user_notification
