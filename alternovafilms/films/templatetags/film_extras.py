from django import template
import re
import films.models as film_models

register = template.Library()

def loop_by_number(number):
    return range(1, number)

def ordering_value(ordering):
    if ordering:
        ordering = re.sub(r'[^A-Za-z0-9_]+', '', ordering)
        ordering = ordering.replace("_", " ")
        return "Sorted by: " + ordering.capitalize()
    else:
        return "Sorted by: Default (Title)"
    
def watched(film_id, user_id):
    try:
        film = film_models.UserFilmVisualization.objects.get(film__id=film_id, user__id=user_id)
    except film_models.UserFilmVisualization.DoesNotExist:
        return False
    return True

def rated(film_id, user_id):
    try:
        film = film_models.UserFilmRating.objects.get(film__id=film_id, user__id=user_id)
    except film_models.UserFilmRating.DoesNotExist:
        return False
    return True

register.filter('watched', watched)
register.filter('rated', rated)
register.filter('loop_by_number', loop_by_number)
register.filter('ordering_value', ordering_value)