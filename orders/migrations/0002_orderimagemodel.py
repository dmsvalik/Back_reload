# Generated by Django 4.1.7 on 2023-05-20 21:19

from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderImageModel",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=orders.models.nameFile
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_id",
                        to="orders.ordermodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображения - заказ пользователя",
                "verbose_name_plural": "Изображения - заказ пользователя",
            },
        ),
    ]
