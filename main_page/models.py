from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserAccountManager(BaseUserManager):
    def create(self, email, name, person_telephone=None, surname=None, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, person_telephone=person_telephone, surname=surname
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, person_telephone=None, surname=None, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, person_telephone=person_telephone, surname=surname
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
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    person_rating = models.IntegerField("Рейтинг клиента", blank=True, null=True)
    person_created = models.DateTimeField("Дата создания аккаунта", auto_now=True)
    person_telephone = models.CharField(
        "Номер телефона", max_length=20, blank=True, null=True
    )
    person_address = models.CharField("Адрес", max_length=200, blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", ]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


class SellerData(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    is_activ = models.BooleanField("Активен / Не активен", default=False)
    company_name = models.CharField("Имя компании", max_length=100, blank=True)
    created_date = models.DateTimeField("Дата создания аккаунта продавца", auto_now=True)
    phone_number = models.CharField("Телефон компании", max_length=20, blank=True)
    requisites = models.CharField(
        "Реквизиты компании", max_length=100, blank=True
    )
    activity_type = models.CharField(
        "Болванка тут должна быть связь с видом деятельности",
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = "Продавцы"
        verbose_name_plural = "Продавцы"


class CooperationOffer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True
    )
    text = models.CharField(
        "Запрос от пользователя", max_length=20, blank=True, null=True
    )
    created = models.DateTimeField("Дата создания обращения", auto_now=True)
