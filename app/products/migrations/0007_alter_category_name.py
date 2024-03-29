# Generated by Django 4.1.7 on 2023-12-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_merge_20231211_1139"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("kitchen", "кухня"),
                    ("table", "стол"),
                    ("bedside_table", "ночной столик"),
                ],
                max_length=50,
                null=True,
                verbose_name="тип - кухня, шкафы, кровати",
            ),
        ),
    ]
