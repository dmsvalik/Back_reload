import uuid

from django.db import models

from app.orders.models import OrderOffer


class FileModel(models.Model):
    """Модель для файлов пользователей."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_name = models.CharField("Имя файла", max_length=250)
    file_path = models.CharField("Путь до файла", max_length=150, blank=True)
    preview_path = models.CharField(
        "Путь до превью файла", max_length=150, blank=True
    )
    date_upload = models.DateTimeField("Дата создания записи", auto_now=True)
    yandex_size = models.PositiveIntegerField(
        "Размер файла в облаке", blank=True
    )
    server_size = models.PositiveIntegerField(
        "Размер файла на сервере", blank=True
    )

    class Meta:
        verbose_name = "Файл пользователя"
        verbose_name_plural = "Файлы пользователей"

    def __str__(self):
        return f"{self.original_name}"


class OfferFileModel(models.Model):
    """Модель связи оффера и файла."""

    file = models.ForeignKey(FileModel, on_delete=models.CASCADE, null=False)
    offer = models.ForeignKey(OrderOffer, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Файл к офферу"
        verbose_name_plural = "Файлы к офферам"

    def __str__(self):
        return f"Файл {str(self.file)} к оффферу с id {self.offer.id}"


class IpFileModel(models.Model):
    """Модель связи IP пользователя и файла."""

    file = models.ForeignKey(FileModel, on_delete=models.CASCADE, null=False)
    ip = models.CharField("IP пользователя", max_length=50)

    class Meta:
        verbose_name = "Файл с IP пользователя"
        verbose_name_plural = "Файлы с IP пользователями"

    def __str__(self):
        return f"Файл {str(self.file)} с IP {self.ip}"


class FileToDelete(models.Model):
    """Промежуточная модель при удалении файлов."""

    file_path = models.CharField("Путь до файла", max_length=150, blank=True)
    preview_path = models.CharField(
        "Путь до превью файла", max_length=150, blank=True
    )

    class Meta:
        verbose_name = "Файл для удаления"
        verbose_name_plural = "Файлы для удаления"

    def __str__(self):
        return f"Файл {str(self.id)} для удаления"
