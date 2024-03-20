from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, InningsSummationForm, PlayerRowForm
from scorerSheet.models import Cell, Game, Team, LineUp, Inning, InningsSummation, TimeOfChange, PlayerRow

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
    PlayerRowFormSet = modelformset_factory(PlayerRow, PlayerRowForm, #formset=CustomLineUpFormSet,
                                         # can_order=True,
                                         # min_num + 1 -> # forms displayed
                                         min_num=9, max_num=9, absolute_max=10)
    game = get_object_or_404(Game, pk=game_id)
    initial_time_of_change, _ = TimeOfChange.objects.get_or_create(inning_in=1, inning_part='T', batsperson=1)
    if request.method == 'POST':
        player_row_formset = PlayerRowFormSet(request.POST,
                                       form_kwargs={'team_id': team_id},
                                       # initial=[{'enter_inning': default_enter_inning}],
                                       )

        if player_row_formset.is_valid():
            for form in player_row_formset:
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
        player_row_formset = PlayerRowFormSet(
            form_kwargs={'team_id': team_id}
        )

    if game.home_team.id == team_id:
        team_name = game.home_team.team_name
    else:
        team_name = game.guest_team.team_name

    context = {
        'player_row_formset': player_row_formset,
        'team_name': team_name,
        'game_id': game_id,
        'team_id': team_id,
    }
    return render(request, 'create_lineup.html', context)


def update_or_create_lineup(form, game) -> PlayerRow:
    """
    Check if lineup is there for player + game,
    if there, update it. If not there, create it.
    """
    player = form.cleaned_data['player']
    batting_pos = int(form.prefix.strip('form-'))
    lineup = LineUp.objects.get_or_create(game=game, team=player.team, batting_pos=batting_pos)[0]
    try:
        player_row = PlayerRow.objects.get(line_up_pos=lineup.pk, player=player.pk)
        # update the lineup
        player_row.jersey_number = form.cleaned_data['jersey_number']
        player_row.defensive_position = form.cleaned_data['defensive_position']
        lineup.save()
        return player_row
    except PlayerRow.DoesNotExist:
        new_player_row = PlayerRow()
        new_player_row.player = player
        new_player_row.jersey_number = form.cleaned_data['jersey_number']
        new_player_row.defensive_position = form.cleaned_data['defensive_position']
        new_player_row.line_up_pos = lineup
        new_player_row.enter_inning = TimeOfChange.objects.get_or_create(inning_in=1, inning_part='T', batsperson=1)[0]
        new_player_row.save()
        return new_player_row


def create_cells_for_lineup(player_row: PlayerRow):
    # I only want to retrieve or get once the inning
    inning_list = []
    for i in range(1, NUMBER_INITIAL_INNINGS+1):
        inning_list.append(Inning.objects.get_or_create(inning=i)[0])

    for i in range(0, NUMBER_INITIAL_INNINGS):
        cell = Cell(inning=inning_list[i], score=player_row.line_up_pos, position=player_row.line_up_pos.batting_pos)
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

    player_row_ids = PlayerRow.objects.select_related(
        "player"
    ).filter(
        line_up_pos__game=game, line_up_pos__team=team
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
        for player_row_id in player_row_ids:
            player_row = LineUp.objects.get(pk=player_row_id)
            cell_formset = CellFormSet(
                request.POST,
                form_kwargs={
                    'team_id': team_id,
                },
                prefix=player_row_id
            )
            cell_formset_list[player_row] = cell_formset
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

        for player_row_id in player_row_ids:
            player_row = PlayerRow.objects.get(pk=player_row_id)
            line_up = player_row.line_up_pos
            cell_formset = CellFormSet(
                queryset=Cell.objects.filter(
                    score=line_up.pk
                ),
                form_kwargs={
                    'team_id': team_id,
                },
                prefix=line_up.pk
            )
            cell_formset_list[player_row] = cell_formset

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
