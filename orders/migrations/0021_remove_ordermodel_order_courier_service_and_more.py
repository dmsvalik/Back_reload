# Generated by Django 4.1.7 on 2023-10-11 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0065_questionnairesection"),
        ("orders", "0020_filedata_order_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordermodel",
            name="order_courier_service",
        ),
        migrations.RemoveField(
            model_name="ordermodel",
            name="order_deliver_price",
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="card_category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.cardmodel",
            ),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="name",
            field=models.CharField(
                max_length=150, null=True, verbose_name="Название заказа"
            ),
        ),
    ]
