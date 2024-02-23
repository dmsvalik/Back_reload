# Generated by Django 4.1.7 on 2024-02-17 07:57

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_alter_useragreement_options_alter_useravatar_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="person_telephone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                unique=True,
                verbose_name="Номер телефона",
            ),
        ),
    ]