# Generated by Django 4.1.7 on 2023-11-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("bedside_table", "ночной столик"),
                    ("table", "стол"),
                    ("kitchen", "кухня"),
                ],
                max_length=50,
                null=True,
                verbose_name="тип - кухня, шкафы, кровати",
            ),
        ),
    ]
