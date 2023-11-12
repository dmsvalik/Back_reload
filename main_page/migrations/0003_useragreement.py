# Generated by Django 4.1.7 on 2023-11-11 08:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_contractoragreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAgreement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(verbose_name='Дата принятия офферты')),
                ('user_account', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)
                 ),
            ],
        ),
    ]
