# Generated by Django 3.1.7 on 2021-03-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210323_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Birthdate'),
        ),
    ]