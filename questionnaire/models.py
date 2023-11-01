from django.db import models


ANSWER_TYPES = {
    ("text_field", 'text_field'),
    ("choice_field", 'choice_field'),
    ("answer_not_required", 'answer_not_required')
}

OPTION_TYPES = {
    ("answer", "answer"),
    ("text_field", "text_field"),
    ("sub_questions", "sub_questions")
}


class QuestionnaireCategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("тип - кухня, шкафы, кровати", max_length=20)

    class Meta:
        verbose_name = "Категория анкеты"
        verbose_name_plural = "Категории анкеты"

    def __str__(self):
        return self.name


class QuestionnaireType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    card_category = models.ForeignKey(QuestionnaireCategory, on_delete=models.CASCADE, null=False)
    questionnaire_type = models.CharField("тип анкеты - короткая, длинная", max_length=20, null=True)
    description = models.CharField("описание анкеты", max_length=300, null=True)

    class Meta:
        verbose_name = "Тип анкеты"
        verbose_name_plural = "Типы анкеты"

    def __str__(self):
        return self.questionnaire_type


class QuestionnaireChapter(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("Раздел опросника", max_length=200)
    questionnaire_type = models.ForeignKey(QuestionnaireType, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Раздел анкеты"
        verbose_name_plural = "Разделы анкеты"

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
    questionnaire_chapter = models.ForeignKey(QuestionnaireChapter, on_delete=models.CASCADE, null=False)
    answer_type = models.CharField("Тип ответа", max_length=200, choices=ANSWER_TYPES)
    file_required = models.BooleanField(default=False)
    # Если будет вопрос относительно опции
    option = models.ForeignKey('Options', blank=True, null=True,
                               on_delete=models.CASCADE, related_name="option_parrent")

    class Meta:
        verbose_name = "Вопрос анкеты"
        verbose_name_plural = "Вопросы анкеты"

    def __str__(self):
        return self.text


class Options(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField("Вопрос", max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    option_type = models.CharField("Тип опции", max_length=200, choices=OPTION_TYPES)
    file_required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Опция вопроса анкеты"
        verbose_name_plural = "Опции вопроса анкеты"

    def __str__(self):
        return self.text
