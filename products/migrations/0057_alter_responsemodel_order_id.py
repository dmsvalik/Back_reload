# Generated by Django 4.1.7 on 2023-06-23 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_ordermodel_options'),
        ('products', '0056_responsemodel_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsemodel',
            name='order_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.ordermodel'),
            preserve_default=False,
        ),
    ]
