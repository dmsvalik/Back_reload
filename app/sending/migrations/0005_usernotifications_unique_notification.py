# Generated by Django 4.1.7 on 2023-12-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sending", "0004_sentnotification"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="usernotifications",
            constraint=models.UniqueConstraint(
                fields=("user", "notification_type"), name="unique_notification"
            ),
        ),
    ]
