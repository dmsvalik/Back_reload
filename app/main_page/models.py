from django.db import models

from app.users.models import UserAccount


class ContractorData(models.Model):
    user = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, primary_key=True
    )
    card_permissions = models.ManyToManyField("products.Category", blank=True)
    is_active = models.BooleanField("Активен / Не активен", default=False)
    company_name = models.CharField("Имя компании", max_length=100, blank=True)
    created_date = models.DateTimeField(
        "Дата создания аккаунта исполнителя", auto_now=True
    )
    phone_number = models.CharField(
        "Телефон компании", max_length=12, blank=True
    )
    requisites = models.CharField(
        "Реквизиты компании", max_length=100, blank=True
    )

    class Meta:
        verbose_name = "Исполнители"
        verbose_name_plural = "Исполнители"


class CooperationOffer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(
        "Имя компании", max_length=100, blank=True, null=True
    )
    telephone = models.CharField(
        "Телефон", max_length=12, blank=True, null=True
    )
    created = models.DateTimeField("Дата создания обращения", auto_now=True)

    class Meta:
        verbose_name = "Предложения на сотрудничество"
        verbose_name_plural = "Предложения на сотрудничество"


class ContactSupport(models.Model):
    user_account = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL, null=True
    )
    user_question = models.CharField(
        "Вопрос от пользователя", max_length=250, blank=True, null=True
    )
    admin_response = models.CharField(
        "Ответ пользователю", max_length=250, blank=True, null=True
    )
    created = models.DateTimeField("Дата создания обращения", auto_now=True)
    resolved = models.BooleanField("Проблема решена?", default=False)

    class Meta:
        verbose_name = "Обращения в поддержку"
        verbose_name_plural = "Обращения в поддержку"


class ContractorAgreement(models.Model):
    user_account = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, primary_key=True
    )
    created_date = models.DateTimeField(
        "Дата подписания соглашения", auto_now_add=True
    )

    class Meta:
        verbose_name = "Соглашение с исполнителем"
        verbose_name_plural = "Соглашения с исполнителями"

    def save(self, *args, **kwargs):
        contractor = ContractorData.objects.get(user_id=self.user_account.id)
        contractor.is_active = True
        contractor.save()
        super().save(*args, **kwargs)
