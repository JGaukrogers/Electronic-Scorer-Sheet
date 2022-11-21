from django.forms import ModelForm, ModelChoiceField, Form

from scorerSheet.models import Cell, Game, Team


class TeamForm(ModelForm):
    class Meta:
        model = Team
#        fields = ['team_name']
        fields = ['club_number',
                  'team_name',
                  'location']


class TeamsDropdown(Form):

    home_team = ModelChoiceField(
        queryset=Team.objects.values_list("team_name", flat=True).distinct(),
        empty_label=None
    )
    guest_team = ModelChoiceField(
        queryset=Team.objects.values_list("team_name", flat=True).distinct(),
        empty_label=None
    )


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
