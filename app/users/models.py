from colorfield.fields import ColorField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .constants import ModelChoices
from .validators import PasswordFieldValidator, NameFieldValidator


# Create your models here.
class UserAccountManager(BaseUserManager):
    """Manager для создания аккаунта пользователя."""

    def create(
        self, email, name, person_telephone=None, surname=None, password=None
    ):
        email = email.lower()

        user = self.model(
            email=email,
            name=name,
            person_telephone=person_telephone,
            surname=surname,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self, email, name, person_telephone, surname, password=None
    ):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            person_telephone=person_telephone,
            surname=surname,
        )

        user.set_password(password)
        user.save()

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        max_length=50,
        validators=[NameFieldValidator(2)],
    )
    surname = models.CharField(
        max_length=50,
        unique=False,
        validators=[NameFieldValidator(2)],
    )
    password = models.CharField(
        "Пароль", max_length=128, validators=[PasswordFieldValidator()]
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    person_rating = models.IntegerField(
        "Рейтинг клиента", blank=True, null=True
    )
    person_created = models.DateTimeField(
        "Дата создания аккаунта", auto_now_add=True
    )
    person_telephone = PhoneNumberField(
        "Номер телефона",
        unique=True,
    )
    person_address = models.CharField(
        "Адрес", max_length=200, blank=True, null=True
    )
    role = models.CharField(
        "Роль",
        max_length=11,
        choices=ModelChoices.ROLES_CHOICES,
        default="client",
    )
    notifications = models.BooleanField("Отправка уведомлений", default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "person_telephone", "surname"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "UserAccount"
        verbose_name_plural = "UserAccount"


class UserAvatar(models.Model):
    """Модель аватара юзера"""

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    color = ColorField()

    class Meta:
        verbose_name = "Аватар пользователя"
        verbose_name_plural = "Аватары пользователей"


class UserQuota(models.Model):
    """Модель для квоты дискового пространства пользователя."""

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    total_cloud_size = models.PositiveIntegerField(default=0)
    total_server_size = models.PositiveIntegerField(default=0)
    total_traffic = models.PositiveIntegerField(default=1000)

    def reset_traffic(self):
        self.total_traffic = 0
        self.save()

    class Meta:
        verbose_name = "Квота пользователя"
        verbose_name_plural = "Квоты пользователей"


class UserAgreement(models.Model):
    """Модель принятия оферты пользователем при регистрации."""

    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True
    )
    date = models.DateField("Дата принятия офферты")

    class Meta:
        verbose_name = "Пользовательское соглашение"
        verbose_name_plural = "Пользовательские соглашения"
