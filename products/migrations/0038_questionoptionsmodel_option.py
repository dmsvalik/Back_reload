# Generated by Django 4.1.7 on 2023-05-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0037_remove_questionoptionsmodel_option"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionoptionsmodel",
            name="option",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="вариант ответа"
            ),
        ),
    ]
