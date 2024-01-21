import uuid

from django.db import models

from app.main_page.models import ContractorData
from app.users.models import UserAccount

from .constants import ORDER_STATE_CHOICES


class OrderModel(models.Model):
    """Модель для создания заказа."""

    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_time = models.DateTimeField(
        "Дата создания заказа", auto_now_add=True
    )
    name = models.CharField("Название заказа", max_length=150, null=True)
    order_description = models.CharField(
        "Описание заказа", max_length=300, blank=True
    )
    questionnaire_type = models.ForeignKey(
        "questionnaire.QuestionnaireType", on_delete=models.CASCADE, null=True
    )
    state = models.CharField(
        verbose_name="Статус",
        choices=ORDER_STATE_CHOICES,
        max_length=50,
        default="draft",
    )

    contractor_selected = models.ForeignKey(
        ContractorData, on_delete=models.SET_NULL, null=True, blank=True
    )
    key = models.UUIDField(
        "Куки-ключ", null=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        verbose_name = "Заказ клиента"
        verbose_name_plural = "Заказ клиента"

    def __str__(self):
        return str(self.id)


class FileData(models.Model):
    """Модель для файлов пользователя."""

    user_account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True
    )
    order_id = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, null=True, blank=True
    )
    yandex_path = models.CharField("Путь в облаке", max_length=150, blank=True)
    server_path = models.CharField(
        "Путь на сервере", max_length=150, blank=True
    )
    date_upload = models.DateTimeField("Дата создания записи", auto_now=True)
    yandex_size = models.CharField(
        "Размер файла в облаке", max_length=150, blank=True
    )
    server_size = models.CharField(
        "Размер файла на сервере", max_length=150, blank=True
    )


class FileAbstractModel(models.Model):
    """Абстрактная модель для файлов."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_name = models.CharField("Имя файла", max_length=250)
    yandex_path = models.CharField("Путь в облаке", max_length=150, blank=True)
    server_path = models.CharField(
        "Путь на сервере", max_length=150, blank=True
    )
    date_upload = models.DateTimeField("Дата создания записи", auto_now=True)
    yandex_size = models.CharField(
        "Размер файла в облаке", max_length=150, blank=True
    )
    server_size = models.CharField(
        "Размер файла на сервере", max_length=150, blank=True
    )

    class Meta:
        abstract = True


class OrderFileData(FileAbstractModel):
    """Модель для файлов заказа пользователя."""

    order_id = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    question_id = models.ForeignKey(
        "questionnaire.Question", on_delete=models.SET_NULL, null=True
    )


class OrderOffer(models.Model):
    """Модель для оферов."""

    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL, null=True
    )
    order_id = models.ForeignKey(
        OrderModel, on_delete=models.SET_NULL, null=True
    )
    offer_create_at = models.DateTimeField(
        "Дата создания офера", auto_now=True
    )
    offer_price = models.CharField(
        "Цена офера", max_length=300, blank=True, default=""
    )
    offer_execution_time = models.CharField(
        "Время выполнения офера", max_length=300, blank=True
    )
    offer_description = models.CharField(
        "Описание офера", max_length=300, blank=True
    )
    offer_status = models.BooleanField("Принят офер или нет", default=False)

    class Meta:
        verbose_name = "Офер"
        verbose_name_plural = "Офер"

    def __str__(self):
        return "офер на заказ №" + " " + str(self.order_id)
