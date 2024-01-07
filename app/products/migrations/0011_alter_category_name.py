# Generated by Django 4.1.7 on 2023-12-29 18:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_alter_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("table", "стол"),
                    ("bedside_table", "ночной столик"),
                    ("kitchen", "кухня"),
                ],
                max_length=50,
                null=True,
                verbose_name="тип - кухня, шкафы, кровати",
            ),
        ),
    ]
