from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.GameView.as_view(), name="games"),
    path('tournaments/', views.TournamentView.as_view(), name="tournaments"),
    path('tournament/<uuid:pk>/', views.TournamentView.as_view(), name="tornament"),
]
