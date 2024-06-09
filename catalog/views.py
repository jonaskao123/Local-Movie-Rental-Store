from django.shortcuts import render

# Create your views here.
from .models import Movie, Director, MovieInstance, Genre, Rating

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

class GenreDetailView(generic.DetailView):
    model = Genre

class GenreListView(generic.ListView):
    model = Genre

class RatingDetailView(generic.DetailView):
    model = Rating

class RatingListView(generic.ListView):
    model = Rating

class MovieInstanceListView(generic.ListView):
    model = MovieInstance

class MovieInstanceDetailView(generic.DetailView):
    model = MovieInstance

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedMoviesByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = MovieInstance
    template_name = 'catalog/movieinstance_list_borrowed_user.html'

    def get_queryset(self):
        return (
            MovieInstance.objects.filter(borrower = self.request.user)
            .filter(status__exact = 'o')
            .order_by('due_back')
        )

from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedMoviesAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = MovieInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/movieinstance_list_borrowed_all.html'

    def get_queryset(self):
        return MovieInstance.objects.filter(status__exact = 'o').order_by('due_back')