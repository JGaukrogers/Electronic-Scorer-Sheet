from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayersForm
from scorerSheet.models import Cell, Player


def update_sheet(request, game_id=0):
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
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            created_game = form.save()
            # TODO: when we create the game I think we also need to make the
            # Score, BattingOrder and Cell objects, then we redirect to
            # update_sheet yielding the right game

            return redirect('add_players', created_game.id)
    else:
        form = GameForm()
    return render(request, 'new_game.html', {'form': form})


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_game')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})


def add_players(request, game_id):
    PlayerFormSet = modelformset_factory(Player, PlayersForm, extra=0)
    if request.method == 'POST':
        home_team_formset = PlayerFormSet(request.POST, prefix='home_team_formset')
        print(home_team_formset) # html with form

        print('=======================================')

        for form in home_team_formset:
            print(form.cleaned_data)

        return redirect('update_sheet')  # todo: add argument / game id
    else:
        PlayerFormSet = modelformset_factory(Player, PlayersForm, extra=0, min_num=9)

        home_team_formset = create_player_formset(PlayerFormSet, request, 'home_team_formset')
        guest_team_formset = create_player_formset(PlayerFormSet, request, 'guest_team_formset')
        context = {'home_team_formset': home_team_formset, 'guest_team_formset': guest_team_formset}

        return render(request, 'add_players.html', context)


def create_player_formset(PlayerFormSet, request, prefix):
    home_team_formset = PlayerFormSet(request.POST or None, prefix=prefix)
    if home_team_formset.is_valid():
        for form in home_team_formset:
            print(form.cleaned_data)
    home_team_formset.save()
    return home_team_formset
