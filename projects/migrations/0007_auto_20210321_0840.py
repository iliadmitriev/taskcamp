# Generated by Django 3.1.7 on 2021-03-21 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210321_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Created'),
        ),
    ]