from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from unidecode import unidecode
import films.models as film_models


@receiver(post_save, sender=film_models.Film)
def create_slug(sender, instance, created, **kwargs):
    """
    create slug signal for Film model when a new film is created
    """
    if created:
        instance.slug = slugify(unidecode(instance.title) + "-" + str(instance.id))
        instance.save()

@receiver(pre_save, sender=film_models.UserFilmRating)
def update_rating(sender, instance, **kwargs):
    """
    update rating signal for UserFilmRating model when a new rating is created

    It will find all ratings for the film and calculate the average rating
    """

    ratings = film_models.UserFilmRating.objects.filter(film = instance.film).exclude(id=instance.id)

    film = film_models.Film.objects.get(id=instance.film.id)
    film.rating = round(((film.rating + instance.rating) / (len(ratings) + 1)), 1)
    film.save()


@receiver(post_save, sender=film_models.UserFilmVisualization)
def update_visualizations(sender, instance, created, **kwargs):
    """
    update visualizations signal for UserFilmVisualization model when a new visualization is created

    It will find all visualizations for the film and update the visualizations counter
    """
    if created:
        instance.film.visualizations += 1
        instance.film.save()