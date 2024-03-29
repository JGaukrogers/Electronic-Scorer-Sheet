# Generated by Django 4.1.5 on 2023-01-05 12:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
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
                ("year", models.PositiveIntegerField()),
                ("game_number", models.CharField(max_length=10)),
                ("location", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Inning",
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
                (
                    "inning",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("club_number", models.IntegerField(unique=True)),
                ("team_name", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                ("pass_number", models.IntegerField(primary_key=True, serialize=False)),
                ("player_name", models.CharField(max_length=50)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LineUp",
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
                (
                    "defensive_position",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(9),
                        ]
                    ),
                ),
                (
                    "enter_inning",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enter_inning",
                        to="scorerSheet.inning",
                    ),
                ),
                (
                    "exit_inning",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exit_inning",
                        to="scorerSheet.inning",
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
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.player",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="game",
            name="guest_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="guest_team",
                to="scorerSheet.team",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="home_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="home_team",
                to="scorerSheet.team",
            ),
        ),
        migrations.CreateModel(
            name="Cell",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "position",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(9),
                        ]
                    ),
                ),
                ("game_moves", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "inning",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.inning",
                    ),
                ),
                (
                    "score",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.lineup",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together={("year", "game_number")},
        ),
    ]
