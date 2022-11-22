from django.forms import ModelForm, ModelChoiceField, Form

from scorerSheet.models import Cell, Game, Team


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
        fields = ['inning',
                  'score',
                  'game_moves']
