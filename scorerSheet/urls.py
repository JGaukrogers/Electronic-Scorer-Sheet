from django.urls import path

from scorerSheet import views

urlpatterns = [
    path('create_team', views.create_team, name='create_team'),
    path('new_game', views.new_game, name='new_game'),
    path('add_players/<int:game_id>', views.add_players, name='add_players'),
    path('add_player/<int:game_id>/<int:team_id>', views.add_player, name='add_player'),
    path('update_sheet', views.update_sheet, name='update_sheet'),
]
