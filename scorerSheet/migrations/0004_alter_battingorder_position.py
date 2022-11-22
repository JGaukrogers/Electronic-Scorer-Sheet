# Generated by Django 4.1.3 on 2022-11-22 13:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scorerSheet", "0003_inning_battingorder_alter_cell_inning"),
    ]

    operations = [
        migrations.AlterField(
            model_name="battingorder",
            name="position",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9),
                ]
            ),
        ),
    ]
