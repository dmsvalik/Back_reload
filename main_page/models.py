from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, User)
from django.db import models


class UserAccountManager(BaseUserManager):

    def create_user(self, email, name, person_telephone, surname, password=None):

        if not email:
            raise ValueError("Почта должна быть указана")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, person_telephone=person_telephone, surname=surname)

        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email, name, password):

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
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
    surname = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    person_rating = models.IntegerField('Рейтинг клиента', null=True)
    person_created = models.DateTimeField('Дата создания аккаунта', auto_now=True)
    person_telephone = models.CharField('Номер телефона', max_length=20, null=True)
    person_address = models.CharField('Адрес', max_length=200, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'person_telephone', 'surname']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
