from django.urls import path

from scorerSheet import views

urlpatterns = [
    path('select_teams', views.select_teams, name='select_teams'),
    path('show_sheet', views.show_sheet, name='show_sheet'),
    path('new_game', views.new_game, name='new_game')
]
