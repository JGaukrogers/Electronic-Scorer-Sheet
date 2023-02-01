from django.contrib import admin

from scorerSheet.models import Inning, Team, Player, Game, Cell, LineUp


@admin.register(Inning)
class InningAdmin(admin.ModelAdmin):
    list_display = ['id', 'inning']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'club_number', 'team_name', 'location']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['pass_number', 'player_name', 'team']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'game_number', 'location']


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'inning', 'score', 'position', 'game_moves']


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    list_display = ['game', 'player', 'defensive_position', 'enter_inning', 'exit_inning']
