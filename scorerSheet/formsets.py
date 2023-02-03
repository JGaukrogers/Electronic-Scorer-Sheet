from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, BaseFormSet


class CustomLineUpFormSet(BaseFormSet):

    def clean(self):
        super().clean()

        players_entered = list()
        for form in self.forms:
            if form.is_valid() and form.has_changed():
                if form.cleaned_data['player'] in players_entered:
                    raise ValidationError('Repeated players detected')
                else:
                    players_entered.append(form.cleaned_data['player'])

        # TODO: leaving players empty there are still errors
        # hence why your code above did not run when below check was done first
        if any(self.errors):
            return
