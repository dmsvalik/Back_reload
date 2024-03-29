# Generated by Django 4.1.7 on 2023-11-18 17:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAccount",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, "the field must contain at least 5 characters"
                            )
                        ],
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "the field must contain at least 2 characters"
                            )
                        ],
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "the field must contain at least 2 characters"
                            )
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "person_rating",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Рейтинг клиента"
                    ),
                ),
                (
                    "person_created",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания аккаунта"
                    ),
                ),
                (
                    "person_telephone",
                    models.CharField(
                        blank=True,
                        max_length=12,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                7, "the field must contain at least 7 numbers"
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "person_address",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Адрес"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("contractor", "Исполнитель"), ("client", "Заказчик")],
                        default="client",
                        max_length=11,
                        verbose_name="Роль",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "UserAccount",
                "verbose_name_plural": "UserAccount",
            },
        ),
        migrations.CreateModel(
            name="EmailSendTime",
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
                    "email",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Почта на которую было отправлено письмо",
                    ),
                ),
                (
                    "api_call",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Api запрос"
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Время отправки запроса на сброс почты",
                    ),
                ),
            ],
            options={
                "verbose_name": "Email - Send Control",
                "verbose_name_plural": "Email - Send Control",
            },
        ),
        migrations.CreateModel(
            name="UserQuota",
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
                ("total_cloud_size", models.PositiveIntegerField(default=0)),
                ("total_server_size", models.PositiveIntegerField(default=0)),
                ("total_traffic", models.PositiveIntegerField(default=1000)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAgreement",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date", models.DateField(verbose_name="Дата принятия офферты")),
                (
                    "user_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
