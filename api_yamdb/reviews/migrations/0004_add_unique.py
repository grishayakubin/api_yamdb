# Generated by Django 4.2 on 2023-04-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0003_rename_verbose_name_to_titles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categories",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="genres",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
