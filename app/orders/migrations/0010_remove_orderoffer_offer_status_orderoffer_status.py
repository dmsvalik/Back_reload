# Generated by Django 4.1.7 on 2024-01-23 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_merge_20240121_2214"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderoffer",
            name="offer_status",
        ),
        migrations.AddField(
            model_name="orderoffer",
            name="status",
            field=models.CharField(
                choices=[
                    ("processed", "В обработке"),
                    ("viewed", "Просмотрен"),
                    ("selected", "Выбран"),
                    ("rejected", "Отклонен"),
                    ("archive", "В архиве"),
                ],
                default="processed",
                max_length=50,
                verbose_name="Статус",
            ),
        ),
    ]