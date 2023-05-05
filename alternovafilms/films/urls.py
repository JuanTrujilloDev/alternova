"""
Films routing configuration file
"""

from django.urls import path
import films.views as views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("films/", views.FilmListView.as_view(), name="films"),
    path("films/detail/<str:slug>/", views.FilmDetailView.as_view(), name="film_detail"),
    path("films/random/", views.RandomFilmView.as_view(), name="random_film"),
]