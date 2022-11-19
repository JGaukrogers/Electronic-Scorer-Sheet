from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render


from scorerSheet.forms import CellForm, GameForm, TeamForm
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
        # create a form instance and populate it with data from the request:
        home_team = request.POST['team_name']
        print(f'home team: {home_team}') #TODO: find out why the team is printed here, but not in the html file
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'sheet.html', {'home_team': home_team})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()
    return render(request, 'new_game.html', {'form': form})


def select_teams(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('select_teams.html')

    else:
        form = TeamForm()
    return render(request, 'select_teams.html', {'form': form})
    pass
