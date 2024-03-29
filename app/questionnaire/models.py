from django.db import models

from app.orders.models import OrderModel
from app.products.models import Category

from .constants import ModelChoice


class QuestionnaireType(models.Model):
    """Модель типа анкеты."""

    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False
    )
    # Тип анкеты пока оставил вводом текста
    type = models.CharField(
        "Тип анкеты - короткая, длинная", max_length=100, null=True
    )
    description = models.CharField(
        "Описание анкеты", max_length=500, null=True
    )
    active = models.BooleanField("Активная анкета", default=True)

    class Meta:
        verbose_name = "Тип анкеты"
        verbose_name_plural = "Типы анкеты"

    def __str__(self):
        return self.type


class QuestionnaireChapter(models.Model):
    """Модель раздела анкеты."""

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("Раздел опросника", max_length=200)
    type = models.ForeignKey(
        QuestionnaireType, on_delete=models.CASCADE, null=False
    )
    position = models.IntegerField("Позиция в анкете", blank=True, null=True)

    class Meta:
        verbose_name = "Раздел анкеты"
        verbose_name_plural = "Разделы анкеты"

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Модель вопроса анкеты.
    Вопрос может быть подвопросом варианта ответов и тогда будет ссылаться
    на этот вариант ответа.
    """

    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
    position = models.IntegerField("Позиция в анкете", blank=True, null=True)
    chapter = models.ForeignKey(
        QuestionnaireChapter, on_delete=models.CASCADE, null=False
    )
    answer_type = models.CharField(
        "Тип ответа", max_length=200, choices=ModelChoice.ANSWER_TYPES
    )
    file_required = models.BooleanField(default=False)
    answer_required = models.BooleanField(default=False)
    # Если будет вопрос относительно опции
    option = models.ForeignKey(
        "Option",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="option_parent",
    )

    class Meta:
        verbose_name = "Вопрос анкеты"
        verbose_name_plural = "Вопросы анкеты"

    def __str__(self):
        return self.text


class Option(models.Model):
    """
    Модель вариантов ответа на вопросы анкеты.
    Вариант ответа может быть окончаельным ответом на вопрос или
    может сообщать о подвопросе.
    """

    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=False,
        related_name="question_parent",
    )
    option_type = models.CharField(
        "Тип опции", max_length=200, choices=ModelChoice.OPTION_TYPES
    )

    class Meta:
        verbose_name = "Опция вопроса анкеты"
        verbose_name_plural = "Опции вопроса анкеты"

    def __str__(self):
        return self.text


class QuestionResponse(models.Model):
    """Модель ответов клиента на вопросы анкеты."""

    id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=False
    )
    response = models.TextField(
        "Ответ по заказу", max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = "Бланк ответов клиента"
        verbose_name_plural = "Бланк ответов клиента"

    def __str__(self):
        return str(self.response)
