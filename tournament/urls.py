from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.GameView.as_view(), name="games"),
    path('tournaments/', views.TournamnetView.as_view(), name="tournaments"),
]
