from django import forms
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


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'team': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        #existing = PricelistProduct.objects.filter(pricelist=pricelist).values_list('product')
        #self.fields['team'].queryset = Player.objects.exclude(id__in=existing)


    # TODO: override queryset to retrieve the right team
