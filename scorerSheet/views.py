from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, LineUpForm
from scorerSheet.models import Cell, Game, Team, LineUp, Inning

NUMBER_INITIAL_INNINGS = 5
NUMBER_PLAYERS_PER_INNING = 9


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
                    new_lineup = save_new_lineup_element(form, game)
                    create_cells_for_lineup(new_lineup)

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


def save_new_lineup_element(form, game):
    # TODO - problem with this: you can't modify existing players, only create new ones
    new_lineup = LineUp()
    new_lineup.game = game
    new_lineup.player = form.cleaned_data['player']
    new_lineup.defensive_position = form.cleaned_data['defensive_position']
    new_lineup.enter_inning = form.cleaned_data['enter_inning']
    new_lineup.save()
    return new_lineup


def create_cells_for_lineup(lineup: LineUp):
    # I only want to retrieve or get once the inning
    inning_list = []
    for i in range(1, NUMBER_INITIAL_INNINGS+1):
        inning_list.append(Inning.objects.get_or_create(inning=i)[0])

    for i in range(0, NUMBER_INITIAL_INNINGS):
        cell = Cell(inning=inning_list[i], score=lineup, position=lineup.defensive_position)
        cell.save()


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
    game = get_object_or_404(Game, pk=game_id)
    team = get_object_or_404(Team, pk=team_id)

    line_up_ids = LineUp.objects.select_related(
        "player"
    ).filter(
        game=game, player__team=team
    ).values_list(
        "id",
        flat=True
    )

    CellFormSet = modelformset_factory(
        Cell,
        CellForm,
        extra=0,
    )

    cell_formset_list = dict()
    if request.method == 'POST':
        for line_up_id in line_up_ids:
            cell_formset = CellFormSet(
                request.POST,
                form_kwargs={
                    'team_id': team_id,
                },
                prefix=line_up_id
            )
            cell_formset_list.append(cell_formset)
            if cell_formset.is_valid():
                cell_formset.save()
    else:

        for line_up_id in line_up_ids:
            line_up = LineUp.objects.get(pk=line_up_id)
            cell_formset = CellFormSet(
                queryset=Cell.objects.filter(
                    score=line_up_id
                ),
                form_kwargs={
                    'team_id': team_id,
                },
                prefix=line_up_id
            )
            cell_formset_list[line_up] = cell_formset

    if game.home_team.id == team_id:
        other_team_id = game.guest_team.id
        which_team = 'Home'
    else:
        other_team_id = game.home_team.id
        which_team = 'Guest'

    context = {
        'team_name': team.team_name,
        'game_id': game_id,
        'other_team_id': other_team_id,
        'team_id': team_id,
        'which_team': which_team,
        'formset_list': cell_formset_list,
    }
    return render(request, "sheet.html", context)
