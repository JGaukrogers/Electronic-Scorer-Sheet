from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayersForm
from scorerSheet.models import Cell


def update_sheet(request, game_id):
    # TODO: this view should retrieve the relevant cells for game_id
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
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('new_game - in form is valid')
            form.save()
            # process the data in form.cleaned_data as required
            # ...

            # TODO: when we create the game I think we also need to make the
            # Score, BattingOrder and Cell objects, then we redirect to
            # update_sheet yielding the right game (added a todo there as well)

            return redirect('add_players')  # add argument / game id
    else:
        form = GameForm()
    return render(request, 'new_game.html', {'form': form})


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            print('create new team')
            form.save()
            return redirect('new_game')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})


def add_players(request):
    if request.method == 'POST':
        return redirect('update_sheet')  # add argument / game id
    else:
        form = PlayersForm() #TODO it should be 9 players + pitcher
        return render(request, 'add_players.html', {'form': form})
