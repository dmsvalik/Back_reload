# Generated by Django 4.1.7 on 2023-10-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_alter_ordermodel_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='order_time',
            field=models.DateTimeField(verbose_name='Дата создания заказа'),
        ),
    ]