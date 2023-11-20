# Generated by Django 4.1.7 on 2023-11-18 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("main_page", "0001_initial"),
        ("products", "0001_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ContractorAgreement",
            fields=[
                (
                    "user_account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата подписания соглашения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Соглашение с исполнителем",
                "verbose_name_plural": "Соглашения с исполнителями",
            },
        ),
        migrations.CreateModel(
            name="CooperationOffer",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Имя компании",
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
                        blank=True, max_length=12, null=True, verbose_name="Телефон"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания обращения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Предложения на сотрудничество",
                "verbose_name_plural": "Предложения на сотрудничество",
            },
        ),
        migrations.CreateModel(
            name="ContractorData",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="Активен / Не активен"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Имя компании"
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания аккаунта исполнителя"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True, max_length=12, verbose_name="Телефон компании"
                    ),
                ),
                (
                    "requisites",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Реквизиты компании"
                    ),
                ),
                (
                    "card_permissions",
                    models.ManyToManyField(blank=True, to="products.category"),
                ),
            ],
            options={
                "verbose_name": "Исполнители",
                "verbose_name_plural": "Исполнители",
            },
        ),
        migrations.AddField(
            model_name="contactsupport",
            name="user_account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
