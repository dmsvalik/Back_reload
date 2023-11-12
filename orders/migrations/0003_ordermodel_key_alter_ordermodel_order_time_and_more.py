# Generated by Django 4.1.7 on 2023-11-08 16:39

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="key",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, null=True, verbose_name="Куки-ключ"
            ),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="order_time",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата создания заказа"
            ),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="state",
            field=models.CharField(
                choices=[
                    ("draft", "Черновик"),
                    ("offer", "Создание предложений"),
                    ("selected", "Исполнитель выбран"),
                    ("completed", "Заказ выполнен"),
                ],
                default="draft",
                max_length=50,
                verbose_name="Статус",
            ),
        ),
    ]