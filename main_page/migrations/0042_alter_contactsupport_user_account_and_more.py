# Generated by Django 4.1.7 on 2023-10-22 16:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_page", "0041_remove_contractordata_activity_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactsupport",
            name="user_account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="cooperationoffer",
            name="user_account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]