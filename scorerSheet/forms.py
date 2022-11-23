from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team, Player


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


class PlayersForm(ModelForm):
    class Meta:
        model = Player
        fields = ['pass_number', 'player_name']