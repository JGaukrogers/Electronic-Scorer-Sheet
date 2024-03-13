from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, LineUpForm, InningsSummationForm
from scorerSheet.formsets import CustomLineUpFormSet
from scorerSheet.models import Cell, Game, Team, LineUp, Inning, InningsSummation, TimeOfChange

NUMBER_INITIAL_INNINGS = 5
NUMBER_PLAYERS_PER_INNING = 9


@login_required
def game_board(request):
    games = Game.objects.select_related(
        "home_team", "guest_team"
    ).all()
    return render(request, 'game_board.html', {'games': games})


@login_required
def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            created_game = form.save()
            return redirect('create_lineup', created_game.id, created_game.home_team.id)
    else:
        form = GameForm()
    return render(request, 'new_game.html', {'form': form})


@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_game')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})


@login_required
def create_lineup(request, game_id, team_id):
    LineUpFormSet = modelformset_factory(LineUp, LineUpForm, formset=CustomLineUpFormSet,
                                         # can_order=True,
                                         # min_num + 1 -> # forms displayed
                                         min_num=9, max_num=9, absolute_max=10)
    game = get_object_or_404(Game, pk=game_id)
    initial_time_of_change, _ = TimeOfChange.objects.get_or_create(inning_in=1, inning_part='T', batsperson=1)
    if request.method == 'POST':
        lineup_formset = LineUpFormSet(request.POST,
                                       form_kwargs={'team_id': team_id},
                                       # initial=[{'enter_inning': default_enter_inning}],
                                       )

        if lineup_formset.is_valid():
            for form in lineup_formset:
                # https://stackoverflow.com/a/29899919
                if form.is_valid() and form.has_changed():
                    new_lineup = update_or_create_lineup(form, game)
                    create_cells_for_lineup(new_lineup)

            # Check if inning summation exists
            create_inning_summations(game, team_id)

            # Redirect
            if game.guest_team.id != team_id:
                team_id = game.guest_team.id
                return redirect('create_lineup', game_id, team_id)
            else:
                return redirect('update_sheet', game_id, game.home_team.id)

    else:
        # upon GET make a new one
        lineup_formset = LineUpFormSet(
            form_kwargs={'team_id': team_id}
        )

    if game.home_team.id == team_id:
        team_name = game.home_team.team_name
    else:
        team_name = game.guest_team.team_name

    context = {
        'team_formset': lineup_formset, # TODO: change name of home_team_formset
        'team_name': team_name,
        'game_id': game_id,
        'team_id': team_id,
    }
    return render(request, 'create_lineup.html', context)


def update_or_create_lineup(form, game) -> LineUp:
    """
    Check if lineup is there for player + game,
    if there, update it. If not there, create it.
    """
    player = form.cleaned_data['player']
    try:
        lineup = LineUp.objects.get(game=game, player=player)
        # update the lineup
        lineup.jersey_number = form.cleaned_data['jersey_number']
        lineup.defensive_position = form.cleaned_data['defensive_position']
        lineup.enter_inning = form.cleaned_data['enter_inning']
        lineup.save()
        return lineup
    except LineUp.DoesNotExist:
        new_lineup = form.save(commit=False)
        new_lineup.game = game
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


def create_inning_summations(game, team_id):
    team = get_object_or_404(Team, pk=team_id)

    inning_summations = InningsSummation.objects.filter(
        game=game, team=team
    )

    if inning_summations.count() == 0:
        innings = Inning.objects.all()
        for inning in innings:
            InningsSummation.objects.create(
                inning=inning,
                team=team,
                game=game,
            )


@login_required
def add_player(request, game_id, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            messages.success(request, 'Player added successfully')
            player.save()
        else:
            messages.error(request, form.errors)
    form = PlayerForm()
    form.fields['team'].initial = team
    context = {'form': form, 'game_id': game_id, 'team_id': team_id}
    return render(request, 'add_player.html', context)


@login_required
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
    InningsSummationFormSet = modelformset_factory(
        InningsSummation,
        InningsSummationForm,
        extra=0,
    )

    cell_formset_list = dict()
    if request.method == 'POST':
        for line_up_id in line_up_ids:
            line_up = LineUp.objects.get(pk=line_up_id)
            cell_formset = CellFormSet(
                request.POST,
                form_kwargs={
                    'team_id': team_id,
                },
                prefix=line_up_id
            )
            cell_formset_list[line_up] = cell_formset
            if cell_formset.is_valid():
                cell_formset.save()

        innings_summation_formset = InningsSummationFormSet(
            request.POST,
            queryset = InningsSummation.objects.filter(
                game=game, team=team
            ),
            prefix='inning_summations'
        )
        if innings_summation_formset.is_valid():
            innings_summation_formset.save()

        messages.success(request, 'Sheet updated')
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

    if not cell_formset_list:
        messages.warning(request, "Need to create lineup first")
        return redirect('create_lineup', game.id, game.home_team.id)

    if game.home_team.id == team_id:
        other_team_id = game.guest_team.id
        which_team = 'Home'
    else:
        other_team_id = game.home_team.id
        which_team = 'Guest'

    innings_summation_formset = InningsSummationFormSet(
        queryset = InningsSummation.objects.filter(
            game=game, team=team
        ),
        prefix='inning_summations'
    )

    context = {
        'team_name': team.team_name,
        'game_id': game_id,
        'other_team_id': other_team_id,
        'team_id': team_id,
        'which_team': which_team,
        'formset_list': cell_formset_list,
        'inning_cells': list(cell_formset_list.values())[0],
        'inning_summations': innings_summation_formset
    }
    return render(request, "sheet.html", context)
