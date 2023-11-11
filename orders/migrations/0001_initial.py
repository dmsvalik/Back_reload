# Generated by Django 4.1.7 on 2023-11-07 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_page", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
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
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Размер файла в облаке"
                    ),
                ),
                (
                    "server_size",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        verbose_name="Размер файла на сервере",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderModel",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "order_time",
                    models.DateTimeField(verbose_name="Дата создания заказа"),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, null=True, verbose_name="Название заказа"
                    ),
                ),
                (
                    "order_description",
                    models.CharField(
                        blank=True, max_length=300, verbose_name="Описание заказа"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("draft", "Черновик"),
                            ("offer", "Создание предложений"),
                            ("selected", "Исполнитель выбран"),
                            ("completed", "Заказ выполнен"),
                        ],
                        max_length=50,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "card_category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                    ),
                ),
                (
                    "contractor_selected",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main_page.contractordata",
                    ),
                ),
                (
                    "user_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ клиента",
                "verbose_name_plural": "Заказ клиента",
            },
        ),
        migrations.CreateModel(
            name="OrderOffer",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "offer_create_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания офера"
                    ),
                ),
                (
                    "offer_price",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=300,
                        verbose_name="Цена офера",
                    ),
                ),
                (
                    "offer_execution_time",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        verbose_name="Время выполнения офера",
                    ),
                ),
                (
                    "offer_description",
                    models.CharField(
                        blank=True, max_length=300, verbose_name="Описание офера"
                    ),
                ),
                (
                    "offer_status",
                    models.BooleanField(
                        default=False, verbose_name="Принят офер или нет"
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="orders.ordermodel",
                    ),
                ),
                (
                    "user_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Офер",
                "verbose_name_plural": "Офер",
            },
        ),
        migrations.CreateModel(
            name="OrderFileData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "original_name",
                    models.CharField(max_length=250, verbose_name="Имя файла"),
                ),
                (
                    "yandex_path",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="Путь в облаке"
                    ),
                ),
                (
                    "server_path",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="Путь на сервере"
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
                    models.IntegerField(verbose_name="Размер файла в облаке, б"),
                ),
                (
                    "server_size",
                    models.IntegerField(verbose_name="Размер файла на сервер, б"),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.ordermodel",
                    ),
                ),
            ],
        ),
    ]
