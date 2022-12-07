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
        super().__init__(*args, **kwargs)
        #existing = PricelistProduct.objects.filter(pricelist=pricelist).values_list('product')
        #self.fields['player'].queryset = Player.objects.filter(team__id=team_id)
    # TODO: override queryset to retrieve the right team
    # Pass the team id in the kwargs, via instance in the form
