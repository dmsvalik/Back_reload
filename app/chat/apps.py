from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.chat"
    label = "chat"

    def ready(self):
        """Добавляем кастомный ресивер сигналов в пространство имен"""
        import app.chat.signals  # noqa
