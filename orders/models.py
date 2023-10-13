from django.db import models

from main_page.models import UserAccount


STATE_CHOICES = (
    ("creating", "Создание заказа"),
    ("auction", "Аукцион"),
    ("new", "Новый"),
    ("confirmed", "Подтвержден"),
    ("assembled", "Собран"),
    ("sent", "Отправлен"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
)

# Заказ создан
# Создание предложений
# Рассмотрение предложений
# Исполнитель выбран


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    order_time = models.DateTimeField("Дата создания заказа", auto_now=True)
    name = models.CharField("Название заказа", max_length=150, null=True)
    order_description = models.CharField("Описание заказа", max_length=300, blank=True)
    card_category = models.ForeignKey("products.CardModel", on_delete=models.CASCADE, null=True)
    state = models.CharField(
        verbose_name="Статус", choices=STATE_CHOICES, max_length=15
    )

    class Meta:
        verbose_name = "Заказ клиента"
        verbose_name_plural = "Заказ клиента"

    def __str__(self):
        return str(self.id)


def nameFile(instance, filename):
    return "/".join(
        [
            "data",
            str(instance.order_id.user_account.id),
            str(instance.order_id.id),
            filename,
        ]
    )


class FileData(models.Model):
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True, blank=True)
    yandex_path = models.CharField("Путь в облаке", max_length=150, blank=True)
    server_path = models.CharField("Путь на сервере", max_length=150, blank=True)
    date_upload = models.DateTimeField("Дата создания записи", auto_now=True)
    yandex_size = models.CharField("Размер файла в облаке", max_length=150, blank=True)
    server_size = models.CharField("Размер файла на сервере", max_length=150, blank=True)


class OrderOffer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True)
    offer_create_at = models.DateTimeField("Дата создания офера", auto_now=True)
    offer_price = models.CharField("Цена офера", max_length=300, blank=True, default="")
    offer_execution_time = models.CharField("Время выполнения офера", max_length=300, blank=True)
    offer_description = models.CharField("Описание офера", max_length=300, blank=True)
    offer_status = models.BooleanField("Принят офер или нет", default=False)

    class Meta:
        verbose_name = "Офер"
        verbose_name_plural = "Офер"

    def __str__(self):
        return "офер на заказ №" + " " + str(self.order_id)
