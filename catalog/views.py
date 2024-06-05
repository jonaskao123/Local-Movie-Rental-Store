from django.shortcuts import render

# Create your views here.
from .models import Movie, Director, MovieInstance, Genre

def index(request):
    num_movies = Movie.objects.all().count()
    num_instances = MovieInstance.objects.all().count()

    num_instances_available = MovieInstance.objects.filter(status__exact = "a").count()
    num_directors = Director.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_movies' : num_movies,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_directors' : num_directors,
        'num_visits' : num_visits,
    }

    return render(request, 'index.html', context = context)

def jonas_kao(request):
    return render(request, 'jonas_kao.html')

from django.views import generic

class MovieListView(generic.ListView):
    model = Movie

class MovieDetailView(generic.DetailView):
    model = Movie

class DirectorListView(generic.ListView):
    model = Director

class DirectorDetailView(generic.DetailView):
    model = Director