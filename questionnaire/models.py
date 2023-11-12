from django.db import models

from orders.models import OrderModel
from products.models import Category

ANSWER_TYPES = {
    ("text_field", 'text_field'),
    ("choice_field", 'choice_field'),
    ("answer_not_required", 'answer_not_required')
}

OPTION_TYPES = {
    ("answer", "answer"),
    ("sub_questions", "sub_questions")
}


class QuestionnaireCategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Категория анкеты"
        verbose_name_plural = "Категории анкеты"

    def __str__(self):
        return self.category.name


class QuestionnaireType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(QuestionnaireCategory, on_delete=models.CASCADE, null=False)
    # Тип анкеты пока оставил вводом текста
    type = models.CharField("Тип анкеты - короткая, длинная", max_length=100, null=True)
    description = models.CharField("Описание анкеты", max_length=500, null=True)

    class Meta:
        verbose_name = "Тип анкеты"
        verbose_name_plural = "Типы анкеты"

    def __str__(self):
        return self.type


class QuestionnaireChapter(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("Раздел опросника", max_length=200)
    type = models.ForeignKey(QuestionnaireType, on_delete=models.CASCADE, null=False)
<<<<<<< HEAD
=======
    position = models.IntegerField("Позиция в анкете", blank=True, null=True)
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104

    class Meta:
        verbose_name = "Раздел анкеты"
        verbose_name_plural = "Разделы анкеты"

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
<<<<<<< HEAD
    position = models.IntegerField("Позиция в анкете")
=======
    position = models.IntegerField("Позиция в анкете", blank=True, null=True)
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
    chapter = models.ForeignKey(QuestionnaireChapter, on_delete=models.CASCADE, null=False)
    answer_type = models.CharField("Тип ответа", max_length=200, choices=ANSWER_TYPES)
    file_required = models.BooleanField(default=False)
    # Если будет вопрос относительно опции
    option = models.ForeignKey('Option', blank=True, null=True,
                                on_delete=models.CASCADE, related_name="option_parent")

    class Meta:
        verbose_name = "Вопрос анкеты"
        verbose_name_plural = "Вопросы анкеты"

    def __str__(self):
        return self.text


class Option(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False,
                                 related_name="question_parent")
    option_type = models.CharField("Тип опции", max_length=200, choices=OPTION_TYPES)

    class Meta:
        verbose_name = "Опция вопроса анкеты"
        verbose_name_plural = "Опции вопроса анкеты"

    def __str__(self):
        return self.text


class QuestionResponse(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    response = models.TextField("Ответ по заказу", max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Бланк ответов клиента"
        verbose_name_plural = "Бланк ответов клиента"

    def __str__(self):
        return str(self.response)
