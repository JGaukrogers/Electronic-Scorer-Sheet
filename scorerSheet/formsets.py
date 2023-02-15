from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


class CustomLineUpFormSet(BaseFormSet):

    def clean(self):
        super().clean()

        self.validate_jersey_number()
        self.validate_defensive_position()

        players_entered = set()
        for form in self.forms:

            # lineup_formset = LineUpFormSet(form_kwargs={'team_id': team_id})
            # default_enter_inning, _ = Inning.objects.get_or_create(inning=1)
    #         if 'player' in form.cleaned_data and 'defensive_position' in form.cleaned_data:
    #             form.cleaned_data['enter_inning'] = default_enter_inning
            if form.is_valid() and form.has_changed():
                if form.cleaned_data['player'] in players_entered:
                    raise ValidationError('Repeated player detected')
                else:
                    players_entered.add(form.cleaned_data['player'])

    def validate_defensive_position(self):
        occupied_positions = [
            form.cleaned_data['defensive_position'] for form in self.forms if "defensive_position" in form.cleaned_data
        ]
        if len(set(occupied_positions)) < len(occupied_positions):
            raise ValidationError('Repeated defense positions detected')

    def validate_jersey_number(self):
        jersey_numbers = [
            form.cleaned_data['jersey_number'] for form in self.forms
        ]
        if jersey_numbers.count(None) > 1:
            raise ValidationError('Multiple empty jersey numbers detected')
        if len(set(jersey_numbers)) < len(jersey_numbers):
            raise ValidationError('Repeated jersey numbers detected')
