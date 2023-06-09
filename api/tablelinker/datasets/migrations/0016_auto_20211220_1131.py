# Generated by Django 3.1 on 2021-12-20 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0015_auto_20211220_1131"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="dataset",
            constraint=models.UniqueConstraint(fields=("dataset_group_id", "version"), name="version_unique"),
        ),
    ]
