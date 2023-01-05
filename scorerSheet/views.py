from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, LineUpForm
from scorerSheet.models import Cell, Game, Team, LineUp, Inning


def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            created_game = form.save()
            return redirect('create_lineup', created_game.id, created_game.home_team.id)
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
    LineUpFormSet = modelformset_factory(LineUp, LineUpForm,
                                         # can_order=True,
                                         min_num=2, max_num=3)
    game = get_object_or_404(Game, pk=game_id)
    default_enter_inning = Inning.objects.get_or_create(inning=1)
    if request.method == 'POST':
        lineup_formset = LineUpFormSet(request.POST,
                                       form_kwargs={'team_id': team_id},
                                       initial=[{'enter_inning': default_enter_inning}])
        if lineup_formset.is_valid():
            for form in lineup_formset:
                # https://stackoverflow.com/a/29899919
                if form.is_valid() and form.has_changed():
                    # TODO - problem with this: you can't modify existing players, only create new ones
                    new_lineup = LineUp()
                    new_lineup.game = game
                    new_lineup.player = form.cleaned_data['player']
                    new_lineup.defensive_position = form.cleaned_data['defensive_position']
                    new_lineup.enter_inning = form.cleaned_data['enter_inning']
                    new_lineup.save()

            if game.guest_team.id != team_id:
                team_id = game.guest_team.id
                return redirect('create_lineup', game_id, team_id)
            else:
                return redirect('update_sheet', game_id, game.home_team.id)

    lineup_formset = LineUpFormSet(form_kwargs={'team_id': team_id})
    for lineup in lineup_formset:
        lineup.fields['enter_inning'].initial = default_enter_inning
    if game.home_team.id == team_id:
        team_name = game.home_team.team_name
    else:
        team_name = game.guest_team.team_name

    context = {
        'team_formset': lineup_formset, #TODO: change name of home_team_formset
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


def update_sheet(request, game_id, team_id):
    # TODO: this view should retrieve the relevant cells for game_id
    # TODO: create two scores for the game: one for home team and one for guest team
    # Cells should belong to one of the two scores

    NUMBER_PLAYERS_PER_INNING = 9

    game = get_object_or_404(Game, pk=game_id)
    line_up_elements = get_list_or_404(LineUp, game=game)  # TODO: could be get_object?

    default_enter_inning, created = Inning.objects.get_or_create(inning=1)

    CellFormSet = modelformset_factory(Cell, CellForm, extra=0, min_num=9, max_num=1*9)

    if request.method == 'POST':
        # TODO: it must be possible to overwrite cells: this is important in case the user enters new data
        formset = CellFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
            formset.save()
        else:
            for form in formset:
                if form.is_valid():
                    form.save()
    else:
        initial = [
            {
                'inning': inning,
                'position': position,
                'score': score,
            }
            for inning, position, score in zip(
                [default_enter_inning] * NUMBER_PLAYERS_PER_INNING,
                range(1, NUMBER_PLAYERS_PER_INNING + 1),
                # To make sure none is preselected: it is better than the first player in the DB is always preselected
                [None] * NUMBER_PLAYERS_PER_INNING
            )
        ]
        formset = CellFormSet(initial=initial)

        # FormSet(initial=[{'id': x.id} for x in some_objects])
        """
        for form in formset:
            form.fields['score'].initial = line_up_elements[0]
            #form.fields['inning'].initial = default_enter_inning
            form.save(commit=False)
        """

    context = {'formset': formset}
    return render(request, "sheet.html", context)
