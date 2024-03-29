# Generated by Django 3.1.7 on 2021-03-21 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_auto_20210321_0803"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now=True, verbose_name="Created"),
                ),
                (
                    "description",
                    models.CharField(max_length=5000, verbose_name="Description"),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.task",
                        verbose_name="Task",
                    ),
                ),
            ],
        ),
    ]
