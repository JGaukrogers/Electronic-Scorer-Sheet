from django.contrib import admin

# Register your models here.
from scorerSheet.models import Inning, Team, Player, Game, Cell, BattingOrder


@admin.register(Inning)
class InningAdmin(admin.ModelAdmin):
    list_display = ['inning']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['club_number', 'team_name', 'location']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['pass_number', 'player_name', 'team']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['year', 'game_number', 'location']


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'inning', 'game_moves', 'score']


@admin.register(BattingOrder)
class BattingOrderAdmin(admin.ModelAdmin):
    list_display = ['game', 'player', 'defensive_position', 'enter_inning', 'exit_inning']
