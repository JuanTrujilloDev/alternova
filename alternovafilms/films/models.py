from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name.capitalize()


class FilmType(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name.capitalize()


# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, blank=False)
    film_type = models.ForeignKey(FilmType, on_delete=models.SET_NULL, null=True)
    visualizations = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
    

class UserFilmRating(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def clean(self) -> None:
        if self.rating < 0 or self.rating > 10:
            raise ValueError("Rating must be between 0 and 10")
        
        rating = UserFilmRating.objects.filter(user=self.user, film=self.film)
        if rating:
            raise ValueError("User has already rated this film")

        return super().clean()


class UserFilmVisualization(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def clean(self) -> None:
        visualization = UserFilmVisualization.objects.filter(user=self.user, film=self.film)
        if visualization:
            raise ValueError("User has already visualized this film")

        return super().clean()
