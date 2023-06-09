# Generated by Django 3.1 on 2020-09-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0009_auto_20200911_2059"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attrtype",
            name="simple_type",
            field=models.IntegerField(
                choices=[(None, "未決定"), (0, "不明"), (100, "文字列"), (200, "数値"), (300, "少数"), (400, "日付")],
                null=True,
                verbose_name="型",
            ),
        ),
        migrations.AlterField(
            model_name="datasetattr",
            name="simple_type",
            field=models.IntegerField(
                choices=[(None, "未決定"), (0, "不明"), (100, "文字列"), (200, "数値"), (300, "少数"), (400, "日付")],
                null=True,
                verbose_name="型",
            ),
        ),
    ]
