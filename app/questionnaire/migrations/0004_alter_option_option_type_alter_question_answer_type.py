# Generated by Django 4.1.7 on 2023-11-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0003_alter_option_option_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="option_type",
            field=models.CharField(
                choices=[("answer", "answer"), ("sub_questions", "sub_questions")],
                max_length=200,
                verbose_name="Тип опции",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_type",
            field=models.CharField(
                choices=[
                    ("text_field", "text_field"),
                    ("answer_not_required", "answer_not_required"),
                    ("choice_field", "choice_field"),
                ],
                max_length=200,
                verbose_name="Тип ответа",
            ),
        ),
    ]
