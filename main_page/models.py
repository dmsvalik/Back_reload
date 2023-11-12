import re

from utils.errorcode import (
    IncorrectEmailCreateUser,
    IncorrectNameCreateUser,
    IncorrectPasswordCreateUser,
    IncorrectSurnameCreateUser,
    IncorrectTelephoneCreateUser,
)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class UserAccountManager(BaseUserManager):
    def create(self, email, name, person_telephone=None, surname=None, password=None):

        if not email:
            raise ValidationError({"error": "Не указана почта"})
        email = email.lower()
        if not re.match(r'^[a-zA-Z-0-9\-.@]{5,50}$', email):
            raise IncorrectEmailCreateUser
        if not person_telephone:
            raise ValidationError({"person_telephone": ["This field is required."]})
        if not surname:
            raise ValidationError({"surname": ["This field is required."]})

        if not re.match(r'^[a-zA-Zа-яА-Я\s\-]{2,20}$', name):
            raise IncorrectNameCreateUser

        if not re.match(r'^[a-zA-Zа-яА-Я\s\-]{2,20}$', surname):
            raise IncorrectSurnameCreateUser

        if person_telephone[0:2] != '+7' or len(person_telephone) != 12 or (person_telephone[1:].isdigit() is False):
            raise IncorrectTelephoneCreateUser

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, person_telephone=person_telephone, surname=surname)

        if not re.match(
                r'^[a-zA-Z-0-9\-~!?@#$%^&*_+(){}<>|.,:\u005B\u002F\u005C\u005D\u0022\u0027]{8,64}$', password
        ) or len(re.findall(r'\d+', password)) == 0:
            raise IncorrectPasswordCreateUser
        user.set_password(password)
        user.save()
        UserQuota.objects.create(user=user)
        UserAgreement.objects.create(user=user)

        return user

    def create_superuser(self, email, name, person_telephone, surname, password=None):
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
    ROLES_CHOICES = [
        ("contractor", 'Исполнитель'),
        ('client', 'Заказчик')
    ]
    email = models.EmailField(max_length=50, unique=True, validators=[
        MinLengthValidator(5, 'the field must contain at least 5 characters')])
    name = models.CharField(max_length=50, validators=[
        MinLengthValidator(2, 'the field must contain at least 2 characters')])
    surname = models.CharField(max_length=50, blank=True, unique=False, null=True, validators=[
        MinLengthValidator(2, 'the field must contain at least 2 characters')])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    person_rating = models.IntegerField("Рейтинг клиента", blank=True, null=True)
    person_created = models.DateTimeField("Дата создания аккаунта", auto_now=True)
    person_telephone = models.CharField(
        "Номер телефона", max_length=12, unique=True, blank=True, null=True,
        validators=[MinLengthValidator(7, 'the field must contain at least 7 numbers')]
    )
    person_address = models.CharField("Адрес", max_length=200, blank=True, null=True)
    role = models.CharField('Роль', max_length=11, choices=ROLES_CHOICES, default='client')

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


class EmailSendTime(models.Model):
    email = models.CharField("Почта на которую было отправлено письмо", max_length=100, blank=True)
    api_call = models.CharField("Api запрос", max_length=100, blank=True)
    timestamp = models.DateTimeField("Время отправки запроса на сброс почты", auto_now=True)

    class Meta:
        verbose_name = "Email - Send Control"
        verbose_name_plural = "Email - Send Control"


class ContractorData(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    card_permissions = models.ManyToManyField("products.Category", blank=True)
    is_active = models.BooleanField("Активен / Не активен", default=False)
    company_name = models.CharField("Имя компании", max_length=100, blank=True)
    created_date = models.DateTimeField("Дата создания аккаунта исполнителя", auto_now=True)
    phone_number = models.CharField("Телефон компании", max_length=12, blank=True)
    requisites = models.CharField("Реквизиты компании", max_length=100, blank=True)

    class Meta:
        verbose_name = "Исполнители"
        verbose_name_plural = "Исполнители"


class CooperationOffer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("Имя компании", max_length=100, blank=True, null=True)
    telephone = models.CharField("Телефон", max_length=12, blank=True, null=True)
    created = models.DateTimeField("Дата создания обращения", auto_now=True)

    class Meta:
        verbose_name = "Предложения на сотрудничество"
        verbose_name_plural = "Предложения на сотрудничество"


class ContactSupport(models.Model):
    user_account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    user_question = models.CharField("Вопрос от пользователя", max_length=250, blank=True, null=True)
    admin_response = models.CharField("Ответ пользователю", max_length=250, blank=True, null=True)
    created = models.DateTimeField("Дата создания обращения", auto_now=True)
    resolved = models.BooleanField("Проблема решена?", default=False)

    class Meta:
        verbose_name = "Обращения в поддержку"
        verbose_name_plural = "Обращения в поддержку"


class UserQuota(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    total_cloud_size = models.PositiveIntegerField(default=0)
    total_server_size = models.PositiveIntegerField(default=0)
    total_traffic = models.PositiveIntegerField(default=1000)

    def reset_traffic(self):
        self.total_traffic = 0
        self.save()


class ContractorAgreement(models.Model):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    created_date = models.DateTimeField("Дата подписания соглашения", auto_now_add=True)

    class Meta:
        verbose_name = "Соглашение с исполнителем"
        verbose_name_plural = "Соглашения с исполнителями"

    def save(self, *args, **kwargs):
        contractor = ContractorData.objects.get(user_id=self.user_account.id)
        contractor.is_active = True
        contractor.save()
        super().save(*args, **kwargs)


class UserAgreement(models.Model):
    """Модель принятия оферты пользователем при регистрации"""
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    date = models.DateField("Дата принятия офферты")
