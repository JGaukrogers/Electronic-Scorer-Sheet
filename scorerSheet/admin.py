from django.contrib import admin

# Register your models here.
from scorerSheet.models import Team, Player, Game, Score, Cell


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['club_number', 'team_name', 'location']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['pass_number', 'player_name', 'team']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['year', 'game_number', 'location']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['game', 'player']


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'inning', 'game_moves', 'player']
