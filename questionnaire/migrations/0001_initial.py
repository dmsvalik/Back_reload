# Generated by Django 4.1.7 on 2023-11-07 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("text", models.CharField(max_length=200, verbose_name="Вопрос")),
                (
                    "option_type",
                    models.CharField(
                        choices=[
                            ("answer", "answer"),
                            ("sub_questions", "sub_questions"),
                        ],
                        max_length=200,
                        verbose_name="Тип опции",
                    ),
                ),
            ],
            options={
                "verbose_name": "Опция вопроса анкеты",
                "verbose_name_plural": "Опции вопроса анкеты",
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("text", models.CharField(max_length=200, verbose_name="Вопрос")),
                ("position", models.IntegerField(verbose_name="Позиция в анкете")),
                (
                    "answer_type",
                    models.CharField(
                        choices=[
                            ("choice_field", "choice_field"),
                            ("text_field", "text_field"),
                            ("answer_not_required", "answer_not_required"),
                        ],
                        max_length=200,
                        verbose_name="Тип ответа",
                    ),
                ),
                ("file_required", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Вопрос анкеты",
                "verbose_name_plural": "Вопросы анкеты",
            },
        ),
        migrations.CreateModel(
            name="QuestionnaireCategory",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория анкеты",
                "verbose_name_plural": "Категории анкеты",
            },
        ),
        migrations.CreateModel(
            name="QuestionResponse",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "response",
                    models.TextField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Ответ по заказу",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.ordermodel",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questionnaire.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Бланк ответов клиента",
                "verbose_name_plural": "Бланк ответов клиента",
            },
        ),
        migrations.CreateModel(
            name="QuestionnaireType",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=100,
                        null=True,
                        verbose_name="Тип анкеты - короткая, длинная",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500, null=True, verbose_name="Описание анкеты"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questionnaire.questionnairecategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип анкеты",
                "verbose_name_plural": "Типы анкеты",
            },
        ),
        migrations.CreateModel(
            name="QuestionnaireChapter",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Раздел опросника"),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questionnaire.questionnairetype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Раздел анкеты",
                "verbose_name_plural": "Разделы анкеты",
            },
        ),
        migrations.AddField(
            model_name="question",
            name="chapter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="questionnaire.questionnairechapter",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="option",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="option_parent",
                to="questionnaire.option",
            ),
        ),
        migrations.AddField(
            model_name="option",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="question_parent",
                to="questionnaire.question",
            ),
        ),
    ]
