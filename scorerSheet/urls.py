from django.urls import path

from scorerSheet import views

urlpatterns = [
    path('', views.show_sheet, name='show_sheet')
]
