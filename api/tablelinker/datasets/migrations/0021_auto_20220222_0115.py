# Generated by Django 3.1 on 2022-02-21 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0020_auto_20220113_1102"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataset", name="current_version",),
        migrations.RemoveField(model_name="datasetgroup", name="current_version",),
        migrations.AddField(
            model_name="dataset", name="name", field=models.CharField(max_length=128, null=True, verbose_name="名前"),
        ),
        migrations.AddField(
            model_name="datasetcurrentversion",
            name="dataset",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to="datasets.dataset"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datasetcurrentversion",
            name="dataset_group",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to="datasets.datasetgroup"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="datasetgroup",
            name="public_level",
            field=models.IntegerField(choices=[(100, "公開"), (10, "非公開")], db_index=True, default=10),
        ),
    ]