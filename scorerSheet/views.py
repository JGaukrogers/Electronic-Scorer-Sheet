from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

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
        cell = Cell(inning = inning_list[i], score=lineup, position = lineup.defensive_position)
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
    # TODO: this view should retrieve the relevant cells for game_id
    # TODO: create two scores for the game: one for home team and one for guest team
    # Cells should belong to one of the two scores

    game = get_object_or_404(Game, pk=game_id)

    line_up_elements = get_list_or_404(LineUp, game=game)  # TODO: could be get_object?
    line_up_elements_for_team = []

    for element in line_up_elements:
        if element.player.team.id == team_id:
            line_up_elements_for_team.append(element)

    CellFormSet = modelformset_factory(Cell, CellForm, extra=0, min_num=NUMBER_PLAYERS_PER_INNING, max_num=1*NUMBER_PLAYERS_PER_INNING)

    if request.method == 'POST':
        # TODO: it must be possible to overwrite cells: this is important in case the user enters new data

        cell_formset_list = []
        for team_line_up in line_up_elements_for_team:
            cell_formset = CellFormSet(request.POST,
                                       form_kwargs={'team_id': team_id, 'player': team_line_up.player.pass_number})
            cell_formset_list.append(cell_formset)

        breakpoint()
        for cell_formset in cell_formset_list:
            if cell_formset.is_valid():
                breakpoint()
                cell_formset.save()
            else:
                breakpoint()
                for cell in cell_formset:
                    if cell.is_valid():
                        cell.save()
        # cell_formset_list = CellFormSet(request.POST, form_kwargs={'team_id': team_id})
        # breakpoint()
        # if cell_formset_list.is_valid():
        #     for form in cell_formset_list:
        #         print(form.cleaned_data)
        #     cell_formset_list.save()
        # else:
        #     # breakpoint()
        #     for form in cell_formset_list:
        #         breakpoint()
        #         if form.is_valid():
        #             form.save()
    else:
        initial = [
            # {
            #     'inning': inning,
            #     'position': position,
            #     'score': score,
            # }
            # for inning, position, score in zip(
            #     [default_enter_inning] * NUMBER_PLAYERS_PER_INNING,
            #     range(1, NUMBER_PLAYERS_PER_INNING + 1),
            #     # To make sure none is preselected: it is better than the first player in the DB is always preselected
            #     [None] * NUMBER_PLAYERS_PER_INNING
            # )
        ]
        cell_formset_list = []
        for team_line_up in line_up_elements_for_team:
            # TODO: cell_formset returns always 30 elements (which are all the existing cells in the DB)
            cell_formset = CellFormSet(initial=initial,
                                       form_kwargs={'team_id': team_id, 'player': team_line_up.player.pass_number})
            breakpoint()
            cell_formset_list.append(cell_formset)
        """
        for form in formset:
            form.fields['score'].initial = line_up_elements[0]
            #form.fields['inning'].initial = default_enter_inning
            form.save(commit=False)
        """

    team_to_show = get_object_or_404(Team, pk=team_id)
    if game.home_team.id == team_id:
        other_team_id = game.guest_team.id
        which_team = 'Home'
    else:
        other_team_id = game.home_team.id
        which_team = 'Guest'



    context = {
        'team_name': team_to_show.team_name,
        'game_id': game_id,
        'other_team_id': other_team_id,
        'which_team': which_team,
        'line_up': cell_formset_list
    }
    return render(request, "sheet.html", context)
