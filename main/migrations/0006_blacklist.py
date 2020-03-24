# Generated by Django 3.0.4 on 2020-03-24 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_auto_20200322_2303"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blacklist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "id_card_no",
                    models.IntegerField(db_index=True, verbose_name="číslo průkazu"),
                ),
                (
                    "reason",
                    models.TextField(blank=True, null=True, verbose_name="zdůvodnění"),
                ),
            ],
        ),
    ]
