from django.urls import path

from scorerSheet import views

urlpatterns = [
    path('', views.new_game, name='home'),
    path('new_game', views.new_game, name='new_game'),
    path('create_team', views.create_team, name='create_team'),
    path('create_lineup/<int:game_id>/<int:team_id>', views.create_lineup, name='create_lineup'),
    path('add_player/<int:game_id>/<int:team_id>', views.add_player, name='add_player'),
    path('update_sheet/<int:game_id>/<int:team_id>', views.update_sheet, name='update_sheet'),
]
