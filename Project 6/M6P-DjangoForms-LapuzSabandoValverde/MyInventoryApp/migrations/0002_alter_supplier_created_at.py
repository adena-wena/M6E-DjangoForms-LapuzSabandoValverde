# Generated by Django 5.1.5 on 2025-03-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MyInventoryApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplier",
            name="created_at",
            field=models.DateTimeField(),
        ),
    ]
