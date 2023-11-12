# Generated by Django 4.1.7 on 2023-11-09 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_alter_option_option_type_alter_question_answer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_type',
            field=models.CharField(choices=[('text_field', 'text_field'), ('choice_field', 'choice_field'), ('answer_not_required', 'answer_not_required')], max_length=200, verbose_name='Тип ответа'),
        ),
    ]