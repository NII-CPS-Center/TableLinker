# Generated by Django 3.1 on 2022-01-11 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0016_auto_20211220_1131"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataset", name="public_level",),
        migrations.AddField(
            model_name="datasetgroup",
            name="public_level",
            field=models.IntegerField(choices=[(100, "公開"), (50, "ログイン済みユーザのみ公開"), (10, "自分のみ")], db_index=True, default=10),
        ),
    ]