# Generated by Django 4.1.5 on 2023-02-14 19:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "scorerSheet",
            "0003_alter_cell_game_move_1_2_alter_cell_game_move_2_3_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="InningsSummation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("runs", models.SmallIntegerField()),
                ("hits", models.SmallIntegerField()),
                ("errors", models.SmallIntegerField()),
                (
                    "left_on_base",
                    models.SmallIntegerField(
                        validators=[django.core.validators.MaxValueValidator(3)]
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.game",
                    ),
                ),
                (
                    "inning",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.inning",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.player",
                    ),
                ),
            ],
        ),
    ]
