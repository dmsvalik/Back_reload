# Generated by Django 4.1.7 on 2023-10-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0065_questionnairesection'),
        ('main_page', '0039_contractordata_card_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractordata',
            name='card_permissions',
            field=models.ManyToManyField(blank=True, to='products.cardmodel'),
        ),
    ]
