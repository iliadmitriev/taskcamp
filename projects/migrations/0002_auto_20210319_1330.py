# Generated by Django 3.1.7 on 2021-03-19 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"verbose_name": "Project", "verbose_name_plural": "Projects"},
        ),
        migrations.AlterModelOptions(
            name="task",
            options={"verbose_name": "Task", "verbose_name_plural": "Tasks"},
        ),
        migrations.AddField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="projects.project",
                verbose_name="Project",
            ),
            preserve_default=False,
        ),
    ]
