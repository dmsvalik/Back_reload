from django.db import models
from main_page.models import UserAccount


class CardModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card_name = models.CharField('тип - кухня, гостиная', max_length=20, null=True)

    class Meta:
        verbose_name = 'Тип комнаты'
        verbose_name_plural = 'Тип комнаты'

    def __str__(self):
        return self.card_name


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card_id = models.ManyToManyField(CardModel)
    category_name = models.CharField('тип мебели - кровать, ящик... ', max_length=20, null=True)

    class Meta:
        verbose_name = 'Тип мебели'
        verbose_name_plural = 'Тип мебели'

    def __str__(self):
        return self.category_name


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True)
    product_price = models.IntegerField('цена предмета', null=True)
    product_size = models.CharField('размеры высота x ширина x длина', max_length=20, null=True)
    product_description = models.CharField('описание', max_length=350, null=True)
    product_units = models.IntegerField('количество предметов в шт.', null=True)

    class Meta:
        verbose_name = 'Предмет для заказа'
        verbose_name_plural = 'Предмет для заказа'

    def __str__(self):
        return self.product_description

class KitModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    product_id = models.ManyToManyField(ProductModel)
    kit_name = models.CharField('название заказа', max_length=20, null=True)

    class Meta:
        verbose_name = 'Заказ состоящий из продуктов'
        verbose_name_plural = 'Заказ состоящий из продуктов'



