from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, LineUpForm
from scorerSheet.models import Cell, Game, Team, LineUp


def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            created_game = form.save()
            return redirect('create_lineup', created_game.id, created_game.home_team.club_number)
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


def create_lineup(request, game_id, team_id):
    LineUpSetForm = modelformset_factory(LineUp, LineUpForm,
                                         min_num=2, max_num=4)
    game = get_object_or_404(Game, pk=game_id)

    if request.method == 'POST':
        lineup_formset = LineUpSetForm(request.POST, form_kwargs={'team_id': team_id})
        if lineup_formset.is_valid():
            for form in lineup_formset:
                # https://stackoverflow.com/a/29899919
                if form.is_valid() and form.has_changed():
                    lineup = form.save(commit=False)
                    lineup.game = game
                    lineup.save()
            if game.guest_team.club_number != team_id:
                team_id = game.guest_team.club_number
                return redirect('create_lineup', game_id, team_id)
            else:
                return redirect('update_sheet', game_id)

    lineup_formset = LineUpSetForm(form_kwargs={'team_id': team_id})
    if game.home_team.club_number == game_id:
        team_name = game.home_team.team_name
    else:
        team_name = game.guest_team.team_name

    context = {
        'home_team_formset': lineup_formset,
        'team_name': team_name,
        'game_id': game_id,
        'team_id': team_id,
    }
    return render(request, 'create_lineup.html', context)


def add_player(request, game_id, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
    data = {'team': team}
    form = PlayerForm(data)
    context = {'form': form, 'game_id': game_id, 'team_id': team_id}
    return render(request, 'add_player.html', context)


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
