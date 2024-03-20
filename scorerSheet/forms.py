from django import forms
from django.forms import ModelForm

from scorerSheet.models import Cell, Game, Team, Player, LineUp, InningsSummation, PlayerRow


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
            self.fields['score'].queryset = LineUp.objects.filter(team=team_id,
                                                                  playerrow__player__pass_number=player_pass_nr)
        else:
            self.fields['score'].queryset = LineUp.objects.filter(team=team_id)
        for field_name in ['game_move_H_1', 'game_move_1_2', 'game_move_2_3', 'game_move_3_H']:
            set_size_for_game_cell(self.fields[field_name])


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
        fields = ['batting_pos']
        widgets = {
            'game': forms.HiddenInput,
            # 'team': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(team__id=team_id)
        self.fields['enter_inning'].initial = 1


class PlayerRowForm(ModelForm):
    class Meta:
        model = PlayerRow
        fields = ['player', 'jersey_number', 'defensive_position']
        widgets = {
            'line_up_pos': forms.HiddenInput,
            'enter_inning': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id')
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(team__id=team_id)
        # self.fields['enter_inning'].initial = 1


class InningsSummationForm(ModelForm):
    class Meta:
        model = InningsSummation
        fields = '__all__'
        widgets = {
            'game': forms.HiddenInput,
            'team': forms.HiddenInput,
            'inning': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['runs', 'hits', 'errors', 'left_on_base']:
            set_size_for_game_cell(self.fields[field_name])


def set_size_for_game_cell(field):
    field.widget.attrs['size'] = 5
