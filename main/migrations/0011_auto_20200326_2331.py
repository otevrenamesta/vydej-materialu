# Generated by Django 3.0.4 on 2020-03-26 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_auto_20200326_2314"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="material",
            options={
                "ordering": ["region_name", "name"],
                "verbose_name": "Materiál",
                "verbose_name_plural": "Materiály",
            },
        ),
        migrations.AlterField(
            model_name="location",
            name="region_name",
            field=models.CharField(max_length=1000, verbose_name="název regionu"),
        ),
        migrations.AlterField(
            model_name="material",
            name="region_name",
            field=models.CharField(max_length=1000, verbose_name="název regionu"),
        ),
    ]
