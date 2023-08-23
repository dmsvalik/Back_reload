# Generated by Django 4.1.7 on 2023-05-18 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0013_alter_productmodel_product_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.categorymodel"
            ),
        ),
        migrations.AlterField(
            model_name="productmodel",
            name="user_account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
