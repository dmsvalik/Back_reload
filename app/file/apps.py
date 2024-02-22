from django.apps import AppConfig


class FileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.file"
    label = "file"

    def ready(self):
        from . import signals  # noqa
