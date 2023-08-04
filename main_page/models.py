from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework.exceptions import ValidationError
import re


def validate_password(password):
    if len(password) < 8 or len(password) > 20:
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[a-zA-Z]", password):
        return False

    if not re.search(r"\W", password):
        return False

    return True


class UserAccountManager(BaseUserManager):
    def create(self, email, name, person_telephone, surname=None, password=None):
        if not email:
            raise ValidationError({"error": "Не указана почта"})

        if not re.match(
                r'^[a-zA-Zа-яА-Я\s\-]{2,50}$', name
        ) or not re.match(
            r'^[a-zA-Zа-яА-Я\s\-]{2,50}$', surname
        ):
            raise ValidationError({"error": "Укажите корректное имя"})

        if person_telephone[0:2] != '+7' or len(
                person_telephone) != 12 or person_telephone[1:].isdigit(

        ) is False:
            raise ValidationError(
                {"error": "Телефон должен начинаться с +7 и иметь 12 символов(цифры)."}
            )

        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, person_telephone=person_telephone, surname=surname
        )
        if validate_password(password):
            user.set_password(password)
        else:
            raise ValidationError({"error": "Укажите корректный пароль"})
        user.save()

        return user

    def create_superuser(self, email, name, person_telephone, surname, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, person_telephone=person_telephone, surname=surname
        )
        if validate_password(password):
            user.set_password(password)
        else:
            raise ValidationError({"error": "Укажите корректный пароль"})
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
    REQUIRED_FIELDS = ["name", "person_telephone"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "UserAccount"
        verbose_name_plural = "UserAccount"


class EmailSendTime(models.Model):
    email = models.CharField("Почта на которую было отправлено письмо", max_length=100, blank=True)
    api_call = models.CharField("Api запрос", max_length=100, blank=True)
    timestamp = models.DateTimeField("Время отправки запроса на сброс почты", auto_now=True)

    class Meta:
        verbose_name = "Email - Send Control"
        verbose_name_plural = "Email - Send Control"


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
