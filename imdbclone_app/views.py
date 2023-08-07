from django.shortcuts import render
from imdbclone_app.models import Movie
from django.http import JsonResponse

# Create your views here.

class MovieDetails:
    
    def movieList(self, request):
        movies = Movie.objects.all()
        data = {
            'movies':list(movies.values())
            }
        
        return JsonResponse(data)
    
    def movieDetails(self, request, movieID):
        movie = Movie.objects.get(pk=movieID)
        data = {
            'name': movie.name,
            'description': movie.description,
            'active': movie.active
        }

        return JsonResponse(data)