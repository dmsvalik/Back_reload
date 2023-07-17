from django.db import models

from main_page.models import UserAccount
from orders.models import OrderModel


class CardModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("тип - кухня, гостиная", max_length=20, null=True)

    class Meta:
        verbose_name = "Тип комнаты - CardModel"
        verbose_name_plural = "Тип комнаты - CardModel"

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card = models.ManyToManyField(CardModel)
    name = models.CharField("тип мебели - кровать, ящик... ", max_length=20, null=True)

    class Meta:
        verbose_name = "Тип мебели - Category"
        verbose_name_plural = "Тип мебели - Category"

    def __str__(self):
        return self.name


# не трогать, возможно пригодится
def nameFile(instance, filename):
    return "/".join(
        [
            "images",
            str(instance.order_id.user_account.id),
            str(instance.order_id.id),
            filename,
        ]
    )


class QuestionsProductsModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=False)
    question = models.CharField(
        "вопрос по заказу", max_length=120, null=True, blank=True
    )
    position = models.IntegerField("номер вопроса по порядку", null=True, blank=True)
    is_image = models.BooleanField('Изображение?', default=False)

    class Meta:
        verbose_name = "Бланк вопросов"
        verbose_name_plural = "Бланк вопросов"

    def __str__(self):
        return "id - " + str(self.id) + " " + self.question


class QuestionOptionsModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    question = models.ForeignKey(
        QuestionsProductsModel, on_delete=models.CASCADE, null=False, blank=True
    )
    option = models.CharField("вариант ответа", max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = "Опции"
        verbose_name_plural = "Опции"

    def __str__(self):
        return "id - " + str(self.id) + " " + self.option


class ResponseModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    order_id = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(
        QuestionsProductsModel, on_delete=models.CASCADE, null=False
    )
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    response = models.CharField(
        "ответ по заказу", max_length=120, null=True, blank=True
    )
    position = models.CharField(
        "номер ответа по порядку", max_length=10, null=True, blank=True
    )
    # image = models.ImageField('Изображение', upload_to= , blank=True, null=True)

    class Meta:
        verbose_name = "Бланк ответов клиента"
        verbose_name_plural = "Бланк ответов клиента"

    def __str__(self):
        return str(self.id)


def iamgeFile(instance, filename):
    return "/".join(
        [
            "images",
            str(instance.response.user_account.id),
            filename,
        ]
    )


class ResponsesImage(models.Model):
    response = models.ForeignKey(ResponseModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to=iamgeFile)