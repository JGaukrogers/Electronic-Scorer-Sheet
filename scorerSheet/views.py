from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from scorerSheet.forms import CellForm, GameForm, TeamForm
from scorerSheet.models import Cell


def show_sheet(request):
    # TODO: this view should get a game id argument to filter the right cells
    # for only that game
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
            # TODO: when we create the game I think we also need to make the
            # Score, BattingOrder and Cell objects, then we redirect to
            # show_sheet yielding the right game

            return redirect('show_sheet')  # add argument / game id
        else:
            print('Form is not valid. Action to be implemented (or not...)')
            # print('new_game - NOT in form is valid')
            # form = GameForm()
            # return render(request, 'new_game.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()
        return render(request, 'new_game.html', {'form': form})


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            print('create new team')
            form.save()
            # TODO: do we need to add the players in this view or make a new
            # dedicated view for that?
            return redirect('new_game')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})
