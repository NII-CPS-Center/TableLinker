# Generated by Django 3.1 on 2020-10-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataset_templates", "0002_auto_20200219_2247"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasettemplate", name="desc", field=models.TextField(max_length=1024, null=True, verbose_name="説明"),
        ),
        migrations.AddField(
            model_name="datasettemplateattr",
            name="desc",
            field=models.TextField(max_length=1024, null=True, verbose_name="説明"),
        ),
    ]
