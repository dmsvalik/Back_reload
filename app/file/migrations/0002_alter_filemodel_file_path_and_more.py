# Generated by Django 4.1.7 on 2024-02-15 20:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filemodel",
            name="file_path",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Путь до файла"
            ),
        ),
        migrations.AlterField(
            model_name="filemodel",
            name="preview_path",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Путь до превью файла"
            ),
        ),
    ]