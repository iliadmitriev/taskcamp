# Generated by Django 3.1.7 on 2021-03-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_auto_20210321_0840"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="description",
            field=models.TextField(max_length=5000, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(
                blank=True, max_length=20000, null=True, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(
                blank=True, max_length=20000, null=True, verbose_name="Description"
            ),
        ),
    ]
