# Generated by Django 4.1.7 on 2023-07-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0025_emailsendtime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailsendtime',
            options={'verbose_name': 'Email - Send Control', 'verbose_name_plural': 'Email - Send Control'},
        ),
        migrations.AddField(
            model_name='emailsendtime',
            name='api_call',
            field=models.CharField(blank=True, max_length=100, verbose_name='Api запрос'),
        ),
    ]
