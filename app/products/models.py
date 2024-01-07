from django.db import models

from .constants import ModelChoice


class Category(models.Model):
    """Модель типа мебели на заказ."""

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(
        "тип - кухня, шкафы, кровати",
        max_length=50,
        null=True,
        choices=ModelChoice.CATEGORY_TYPES,
    )
    active = models.BooleanField("Активная категория", default=True)

    class Meta:
        verbose_name = "Тип мебели на заказ - Category"
        verbose_name_plural = "Тип мебели на заказ - Category"

    def __str__(self):
        return self.name
