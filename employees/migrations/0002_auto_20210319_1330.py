# Generated by Django 3.1.7 on 2021-03-19 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="employee",
            options={"verbose_name": "Employee", "verbose_name_plural": "Employees"},
        ),
    ]
