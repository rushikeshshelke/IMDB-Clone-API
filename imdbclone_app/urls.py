from django.urls import path
from imdbclone_app.views import MovieDetails

urlpatterns = [
    path('list/',MovieDetails().movieList, name='movie-list'),
    path('<int:movieID>',MovieDetails().movieDetails, name="movie-details"),
]
