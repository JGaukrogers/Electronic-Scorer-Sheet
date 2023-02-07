from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


class CustomLineUpFormSet(BaseFormSet):

    def clean(self):
        super().clean()

        players_entered = list()
        occupied_positions = list()
        for form in self.forms:

            # lineup_formset = LineUpFormSet(form_kwargs={'team_id': team_id})
            # default_enter_inning, _ = Inning.objects.get_or_create(inning=1)
    #         if 'player' in form.cleaned_data and 'defensive_position' in form.cleaned_data:
    #             form.cleaned_data['enter_inning'] = default_enter_inning
            if form.is_valid() and form.has_changed():
                if form.cleaned_data['player'] in players_entered:
                    raise ValidationError('Repeated player detected')
                elif form.cleaned_data['defensive_position'] in occupied_positions:
                    raise ValidationError('Repeated position detected')
                else:
                    players_entered.append(form.cleaned_data['player'])
                    occupied_positions.append(form.cleaned_data['defensive_position'])