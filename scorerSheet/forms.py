from django import forms
from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team, Player, LineUp


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class CellForm(ModelForm):
    class Meta:
        model = Cell
        fields = '__all__'  # inning, score, position, game_moves


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'team': forms.HiddenInput,
        }


class LineUpForm(ModelForm):
    class Meta:
        model = LineUp
        fields = ['player', 'defensive_position', 'enter_inning', 'exit_inning']
        widgets = {
            'game': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(team__id=team_id)
