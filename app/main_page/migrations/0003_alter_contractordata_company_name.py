# Generated by Django 4.1.7 on 2024-01-21 17:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_page", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractordata",
            name="company_name",
            field=models.CharField(max_length=100, verbose_name="Имя компании"),
        ),
    ]
