from django.db import models

from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 200, help_text = 'Enter a movie genre (e.g. Action, Comedy)')

    def __str__(self):
        return self.name

class Rating(models.Model):
    name = models.CharField(max_length = 200, unique = True, help_text="Enter the movie's rating (1.0 to 10.0)")

    def get_absolute_url(self):
        return reverse('rating-detail', args = [str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'rating_name_case_insensitive_unique',
                violation_error_message = 'Rating already exists (case insensitive match)'
            ),
        ]
class Movie(models.Model):
    title = models.CharField(max_length = 200)
    director = models.ForeignKey('Director', on_delete = models.SET_NULL, null = True)

    summary = models.TextField(max_length = 1000, help_text = 'Enter a brief description of the movie')
    imdb_id = models.CharField('IMDB_ID', max_length = 13, help_text='9 Characters <a href="https://developer.imdb.com/documentation/key-concepts/'
                                      '">IMDB ID</a>')

    rating = models.ForeignKey('Rating', on_delete = models.SET_NULL, null = True)
    genre = models.ManyToManyField(Genre, help_text = 'Select a genre for this movie')

    class Meta:
        ordering = ['title', 'director']

    def __str__(self):
        return self.title

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse("movie-detail", args = [str(self.id)])

import uuid

class MovieInstance(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = "Unique ID for this particular movie across whole library")
    movie = models.ForeignKey("Movie", on_delete = models.SET_NULL, null = True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True, blank = True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = "Movie availability",
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.id} ({self.movie.title})"

class Director(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField("Died", null = True, blank = True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("director-detail", args = [str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
