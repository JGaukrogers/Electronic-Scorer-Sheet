from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render


from scorerSheet.forms import CellForm, GameForm, TeamForm, TeamsDropdown
from scorerSheet.models import Cell, Team


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
            create_new_team(request)
            print('new_game - NOT in form is valid')
            form = GameForm()
            return render(request, 'new_game.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()
        return render(request, 'new_game.html', {'form': form})


def create_new_team(request):
    new_team = Team()
    new_team.club_number = request.POST['club_number']
    new_team.team_name = request.POST['team_name']
    new_team.location = request.POST['location']
    new_team.save()


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('create_team.html')
    else:
        form = TeamForm()
        return render(request, 'create_team.html', {'form': form})
