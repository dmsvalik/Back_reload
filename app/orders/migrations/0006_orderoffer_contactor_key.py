# Generated by Django 4.1.7 on 2024-01-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_alter_ordermodel_user_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderoffer",
            name="contactor_key",
            field=models.IntegerField(default=1, verbose_name="Номер исполнителя"),
            preserve_default=False,
        ),
    ]