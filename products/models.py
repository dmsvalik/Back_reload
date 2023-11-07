from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("тип - кухня, шкафы, кровати", max_length=50, null=True)

    class Meta:
        verbose_name = "Тип мебели на заказ - Category"
        verbose_name_plural = "Тип мебели на заказ - Category"

    def __str__(self):
        return self.name
