# Generated by Django 4.1.7 on 2023-07-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_ordermodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderoffer',
            name='offer_price',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Цена офера'),
        ),
    ]
