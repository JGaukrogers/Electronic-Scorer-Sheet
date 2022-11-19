from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['club_number',
                  'team_name',
                  'location']


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['home_team',
                  'guest_team',
                  'location',
                  'year',
                  'game_number']


class CellForm(ModelForm):
    class Meta:
        model = Cell
        fields = ['inning',
                  'score',
                  'game_moves']
