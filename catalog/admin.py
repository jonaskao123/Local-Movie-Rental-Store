from django.contrib import admin

# Register your models here.
from .models import Director, Genre, Movie, MovieInstance, Rating

admin.site.register(Genre)
admin.site.register(Rating)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Director, DirectorAdmin)

class MovieInstanceInline(admin.TabularInline):
    model = MovieInstance

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'display_genre')
    inlines = [MovieInstanceInline]

@admin.register(MovieInstance)
class MovieInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('movie', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )