# Generated by Django 4.1.7 on 2023-10-01 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_filedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.ordermodel'),
        ),
    ]
