# Generated by Django 4.1.2 on 2022-12-07 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scorerSheet", "0005_battingorder_game"),
    ]

    operations = [
        migrations.RenameField(
            model_name="battingorder",
            old_name="position",
            new_name="defensive_position",
        ),
    ]