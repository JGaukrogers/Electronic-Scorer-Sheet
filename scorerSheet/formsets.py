from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


class CustomLineUpFormSet(BaseFormSet):

    def clean(self):
        super().clean()

        self.validate_jersey_number()
        self.validate_defensive_position()
        self.validate_players_entered()

    def validate_players_entered(self):
        players_entered = [
            form.cleaned_data['player'] for form in self.forms if "player" in form.cleaned_data
        ]
        if len(set(players_entered)) < len(players_entered):
            raise ValidationError('Repeated players detected')

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
