# Generated by Django 4.1.7 on 2023-12-07 04:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_category_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Активная категория"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("kitchen", "кухня"),
                    ("bedside_table", "ночной столик"),
                    ("table", "стол"),
                ],
                max_length=50,
                null=True,
                verbose_name="тип - кухня, шкафы, кровати",
            ),
        ),
    ]