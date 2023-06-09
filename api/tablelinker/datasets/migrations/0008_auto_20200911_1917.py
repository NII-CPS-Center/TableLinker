# Generated by Django 2.2.15 on 2020-09-11 10:17

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0007_auto_20200831_2030"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttrType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("key", models.CharField(db_index=True, max_length=128, verbose_name="キー")),
                ("name", models.CharField(db_index=True, max_length=128, verbose_name="名前")),
                ("index", models.IntegerField(verbose_name="順序")),
                ("simple_type", models.IntegerField(default=0, null=True, verbose_name="型")),
            ],
        ),
        migrations.AddField(
            model_name="datasetattr", name="simple_type", field=models.IntegerField(default=0, null=True, verbose_name="型"),
        ),
        migrations.AddField(
            model_name="datasetattr",
            name="attr_type",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="dataset_attr", to="datasets.AttrType"
            ),
        ),
    ]
