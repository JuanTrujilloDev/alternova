import films.models as film_models
from django.contrib import admin

# Register your models here.
admin.site.register(film_models.Genre)
admin.site.register(film_models.FilmType)
admin.site.register(film_models.Film)
admin.site.register(film_models.UserFilmRating)
admin.site.register(film_models.UserFilmVisualization)
