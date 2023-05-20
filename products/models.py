from django.db import models
from main_page.models import UserAccount


class CardModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField('тип - кухня, гостиная', max_length=20, null=True)

    class Meta:
        verbose_name = 'Тип комнаты - CardModel'
        verbose_name_plural = 'Тип комнаты - CardModel'

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card = models.ManyToManyField(CardModel)
    name = models.CharField('тип мебели - кровать, ящик... ', max_length=20, null=True)

    class Meta:
        verbose_name = 'Тип мебели - Category'
        verbose_name_plural = 'Тип мебели - Category'

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=False,  blank=True)
    product_price = models.IntegerField('цена предмета', null=True, blank=True)
    product_size = models.CharField('размеры высота x ширина x длина', max_length=20, null=True, blank=True)
    product_description = models.CharField('описание', max_length=350, null=True, blank=True)
    product_units = models.IntegerField('количество предметов в шт.', null=True, blank=True)
    is_ended = models.BooleanField('завершено ли создание предмета заказа?', default=False)

    class Meta:
        verbose_name = 'Предмет для заказа'
        verbose_name_plural = 'Предмет для заказа'

    def __str__(self):
        return str(self.id)


# создаем путь - папка image далее папка(id пользователя), далее папка(id продукта)
def nameFile(instance, filename):
    return '/'.join(['images', str(instance.product_id.user_account.id), str(instance.product_id.id), filename])

class ProductImageModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    product_id = models.ForeignKey(ProductModel, related_name='product_id', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)

    class Meta:
        verbose_name = 'Изображения - продукты пользователя'
        verbose_name_plural = 'Изображения - продукты пользователя'

    def __str__(self):
        return str(self.id)

