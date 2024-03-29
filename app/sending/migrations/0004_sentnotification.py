# Generated by Django 4.1.7 on 2023-12-02 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sending", "0003_alter_usernotifications_notification_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="SentNotification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата уведомления"
                    ),
                ),
                (
                    "theme",
                    models.CharField(max_length=200, verbose_name="Тема уведомления"),
                ),
                (
                    "type",
                    models.CharField(max_length=200, verbose_name="Тип уведомления"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отправленное уведомление",
                "verbose_name_plural": "Отправленные уведомления",
            },
        ),
    ]
