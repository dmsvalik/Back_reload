# Generated by Django 4.1.7 on 2024-02-20 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("file", "0002_alter_filemodel_file_path_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="IpFileModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.CharField(max_length=50, verbose_name="IP пользователя")),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="file.filemodel"
                    ),
                ),
            ],
            options={
                "verbose_name": "Файл с IP пользователя",
                "verbose_name_plural": "Файлы с IP пользователями",
            },
        ),
    ]
