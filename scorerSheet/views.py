from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render


from scorerSheet.forms import CellForm, GameForm, TeamForm, TeamsDropdown
from scorerSheet.models import Cell


def show_sheet(request):
    CellFormSet = modelformset_factory(Cell, CellForm, extra=0)
    if request.method == 'POST':
        formset = CellFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
            formset.save()
    else:
        formset = CellFormSet()

    context = {'formset': formset}
    return render(request, "sheet.html", context)


def new_game(request):
#    import pdb; pdb.set_trace()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('new_game - in post')
        team_list = TeamsDropdown()
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('new_game - in form is valid')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'sheet.html', {'team_list': team_list})
        else:
            print('new_game - NOT in form is valid')
            return render(request, 'new_game.html', {'team_list': team_list})

    # if a GET (or any other method) we'll create a blank form
    else:
        print('new_game - NOT in post')
        form = GameForm()
        return render(request, 'new_game.html', {'form': form})


def select_teams(request):
    if request.method == 'POST':
        print('select_teams - in post')
        form = TeamForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('select_teams.html')

    else:
        print('select_teams - NOT in post')
        form = TeamForm()
        team_list = TeamsDropdown()
        return render(request, 'select_teams.html', {'form': form, 'team_list': team_list})
