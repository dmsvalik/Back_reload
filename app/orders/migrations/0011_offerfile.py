# Generated by Django 4.1.7 on 2024-02-08 13:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0010_worksheetfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="OfferFile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "original_name",
                    models.CharField(max_length=250, verbose_name="Имя файла"),
                ),
                (
                    "yandex_path",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Путь в облаке"
                    ),
                ),
                (
                    "server_path",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Путь на сервере"
                    ),
                ),
                (
                    "date_upload",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания записи"
                    ),
                ),
                (
                    "yandex_size",
                    models.PositiveIntegerField(
                        blank=True, verbose_name="Размер файла в облаке"
                    ),
                ),
                (
                    "server_size",
                    models.PositiveIntegerField(
                        blank=True, verbose_name="Размер файла на сервере"
                    ),
                ),
                (
                    "offer_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="orders.orderoffer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]