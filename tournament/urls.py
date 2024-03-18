from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.GameView.as_view(), name="games"),
    path('tournaments/', views.TournamentView.as_view(), name="tournaments"),
    path('tournament/<uuid:pk>/', views.TournamentView.as_view(), name="tornament"),
    path('tournaments/joined/', views.JoinedTournamentView.as_view(), name="joined-tournaments"),
    path('tournaments/hosted/', views.HostedTournamentView.as_view(), name="hosted-tournaments"),
    path('tournament/leave/<uuid:pk>/', views.LeaveTournamentView.as_view(), name="leave-tournaments"),
    path('tournament/join/<uuid:pk>/', views.JoinTournamentView.as_view(), name="join-tournament"),
]
