from django.forms import ModelForm

from scorerSheet.models import Cell


class CellForm(ModelForm):
    class Meta:
        model = Cell
        fields = ['inning',
                  'score',
                  'game_moves']
