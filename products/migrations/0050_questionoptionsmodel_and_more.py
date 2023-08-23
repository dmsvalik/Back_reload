# Generated by Django 4.1.7 on 2023-05-29 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0049_merge_20230529_1839"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionOptionsModel",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "option",
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True,
                        verbose_name="вариант ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Опции",
                "verbose_name_plural": "Опции",
            },
        ),
        migrations.RenameField(
            model_name="questionsproductsmodel",
            old_name="category_id",
            new_name="category",
        ),
        migrations.RenameField(
            model_name="responsemodel",
            old_name="id_question",
            new_name="question",
        ),
        migrations.DeleteModel(
            name="QuestionOptionsKitchenModel",
        ),
        migrations.AddField(
            model_name="questionoptionsmodel",
            name="question",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.questionsproductsmodel",
            ),
        ),
    ]
