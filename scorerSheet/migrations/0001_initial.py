# Generated by Django 4.1.2 on 2022-11-16 17:47

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
            name="Player",
            fields=[
                ("pass_number", models.IntegerField(primary_key=True, serialize=False)),
                ("player_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("club_number", models.IntegerField(primary_key=True, serialize=False)),
                ("team_name", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Score",
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
            model_name="player",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="scorerSheet.team"
            ),
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
                ("timestamp", models.TimeField()),
                (
                    "inning",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                ("game_moves", models.CharField(max_length=50)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scorerSheet.score",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together={("year", "game_number")},
        ),
    ]
