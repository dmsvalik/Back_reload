# Generated by Django 4.1.7 on 2023-11-05 10:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0066_alter_cardmodel_options_alter_cardmodel_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questionnairemodel",
            name="card_category",
        ),
        migrations.RemoveField(
            model_name="questionnairesection",
            name="questionnaire_type",
        ),
        migrations.RemoveField(
            model_name="questionoptionsmodel",
            name="question",
        ),
        migrations.RemoveField(
            model_name="questionsproductsmodel",
            name="category",
        ),
        migrations.RemoveField(
            model_name="responsemodel",
            name="order_id",
        ),
        migrations.RemoveField(
            model_name="responsemodel",
            name="question",
        ),
        migrations.RemoveField(
            model_name="responsemodel",
            name="user_account",
        ),
        migrations.RemoveField(
            model_name="responsesimage",
            name="response",
        ),
        migrations.DeleteModel(
            name="CategoryModel",
        ),
        migrations.DeleteModel(
            name="QuestionnaireModel",
        ),
        migrations.DeleteModel(
            name="QuestionnaireSection",
        ),
        migrations.DeleteModel(
            name="QuestionOptionsModel",
        ),
        migrations.DeleteModel(
            name="QuestionsProductsModel",
        ),
        migrations.DeleteModel(
            name="ResponseModel",
        ),
        migrations.DeleteModel(
            name="ResponsesImage",
        ),
    ]
