# Generated by Django 4.1.7 on 2023-05-26 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0045_alter_questionoptionskitchenmodel_question_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionoptionskitchenmodel",
            name="question_id",
            field=models.ForeignKey(
                limit_choices_to={"category_id_id": "кухня"},
                on_delete=django.db.models.deletion.CASCADE,
                to="products.questionsproductsmodel",
            ),
        ),
    ]
