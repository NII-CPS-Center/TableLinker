# Generated by Django 3.2.15 on 2022-09-22 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0026_auto_20220601_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetcurrentversion',
            name='dataset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_version', to='datasets.dataset'),
        ),
        migrations.AlterField(
            model_name='datasetcurrentversion',
            name='dataset_group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_version', to='datasets.datasetgroup'),
        ),
    ]
