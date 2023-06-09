# Generated by Django 3.1 on 2022-06-01 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0025_auto_20220305_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetgroup',
            name='public_level',
            field=models.IntegerField(choices=[(100, '公開中'), (10, '非公開')], db_index=True, default=10),
        ),
        migrations.AddConstraint(
            model_name='datasetsource',
            constraint=models.UniqueConstraint(fields=('dataset_group',), name='unique_dataset_source_dataset_group'),
        ),
    ]
