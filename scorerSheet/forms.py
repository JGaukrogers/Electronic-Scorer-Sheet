from django import forms
from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team, Player, LineUp, InningsSummation


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

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        player_pass_nr = None
        if 'player' in kwargs:
            player_pass_nr = kwargs.pop('player')
        super().__init__(*args, **kwargs)
        if player_pass_nr:
            self.fields['score'].queryset = LineUp.objects.filter(player__team=team_id,
                                                                  player__pass_number=player_pass_nr)
        else:
            self.fields['score'].queryset = LineUp.objects.filter(player__team=team_id)


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
        fields = ['jersey_number', 'player', 'defensive_position', 'enter_inning', 'exit_inning']
        widgets = {
            'game': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(team__id=team_id)
        self.fields['enter_inning'].initial = 1


class InningsSummationForm(ModelForm):
    class Meta:
        model = InningsSummation
        fields = '__all__'
        widgets = {
            'game': forms.HiddenInput,
            'team': forms.HiddenInput,
            'inning': forms.HiddenInput,
        }
