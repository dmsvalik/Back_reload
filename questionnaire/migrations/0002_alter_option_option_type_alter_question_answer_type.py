# Generated by Django 4.1.7 on 2023-11-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="option_type",
            field=models.CharField(
                choices=[("sub_questions", "sub_questions"), ("answer", "answer")],
                max_length=200,
                verbose_name="Тип опции",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_type",
            field=models.CharField(
                choices=[
                    ("answer_not_required", "answer_not_required"),
                    ("text_field", "text_field"),
                    ("choice_field", "choice_field"),
                ],
                max_length=200,
                verbose_name="Тип ответа",
            ),
        ),
    ]