from django import forms
from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team, Player, BattingOrder


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
        fields = '__all__'


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'team': forms.HiddenInput,
        }


class BattingOrderForm(ModelForm):
    class Meta:
        model = BattingOrder
        fields = '__all__'
        widgets = {
            'game': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(team__club_number=team_id)
