# Generated by Django 3.1 on 2022-01-13 02:02

import datasets.models.dataset
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0019_dataset_mtab"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataset", name="mtab",),
        migrations.AddField(
            model_name="dataset",
            name="mtab_file",
            field=models.FileField(
                blank=True, null=True, upload_to=datasets.models.dataset.mtab_file_name_by_data, verbose_name="mtab情報"
            ),
        ),
    ]