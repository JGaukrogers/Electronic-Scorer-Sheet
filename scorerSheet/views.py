from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from scorerSheet.forms import CellForm, GameForm, TeamForm, PlayerForm, BattingOrderForm
from scorerSheet.models import Cell, Game, Team, BattingOrder


def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            created_game = form.save()
            # TODO: when we create the game I think we also need to make the
            # Score, BattingOrder and Cell objects, then we redirect to
            # update_sheet yielding the right game

            return redirect('create_batting_order', created_game.id, created_game.home_team.club_number)
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


def create_batting_order(request, game_id, team_id):
    # TODO: this leads to duplicate players, so let's have a simple view for
    # adding players one by one (like create_team view), then this view is
    # really for BattingOrder, which if you put that in modelformset_factory
    # below game and player become dropdowns and user adds position, etc in
    # tabular form -- this new model formset should support editing as well
    BattingOrderSetForm = modelformset_factory(BattingOrder, BattingOrderForm,
                                               min_num=2, max_num=4)
    game = get_object_or_404(Game, pk=game_id)

    if request.method == 'POST':
        batting_order_formset = BattingOrderSetForm(request.POST, form_kwargs={'team_id': team_id})
        # todo: solve problem: for some reason batting_order_formset is never valid right now
        if batting_order_formset.is_valid():
            for form in batting_order_formset:
                # https://stackoverflow.com/a/29899919
                if form.is_valid() and form.has_changed():
                    batting_order = form.save(commit=False)
                    batting_order.game = game
                    batting_order.save()

            return redirect('update_sheet', game_id)

    batting_order_formset = BattingOrderSetForm(form_kwargs={'team_id': team_id})
    context = {
        'home_team_formset': batting_order_formset,
        'team_name': game.home_team.team_name,
        'game_id': game_id,
        'team_id': team_id,
    }
    return render(request, 'create_batting_order.html', context)


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
