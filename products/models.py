from django.db import models


class CardModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card_name = models.CharField('тип - кухня, гостиная', max_length=20, null=True)


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account_id = models.ManyToManyField(CardModel)
    category_name = models.CharField('тип мебели - кровать, ящик... ', max_length=20, null=True)

