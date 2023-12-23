# Generated by Django 4.1.7 on 2023-12-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0009_merge_20231214_1931"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("table", "стол"),
                    ("kitchen", "кухня"),
                    ("bedside_table", "ночной столик"),
                ],
                max_length=50,
                null=True,
                verbose_name="тип - кухня, шкафы, кровати",
            ),
        ),
    ]
