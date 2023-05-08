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

def ordered_page_number(page_number, ordering):
    page_number = str(page_number)
    if ordering:
        return f"?ordering={ordering}&page={page_number}"
    
    return f"?page={page_number}"


    

def filtered_page_number(filtering_data, page_number):
    genres = filtering_data.get('genres', None)
    title = filtering_data.get('title', None)
    film_type = filtering_data.get('film_type', None)

    link = []
    if genres:
        link.append(f"genres={genres}")

    if title:
        link.append(f"title={title}")

    if film_type:
        link.append(f"film_type={film_type}")

    if link:
        link = "&".join(link)
        return f"?{link}&page={page_number}"

    
    

register.filter('watched', watched)
register.filter('rated', rated)
register.filter('loop_by_number', loop_by_number)
register.filter('ordering_value', ordering_value)
register.filter('ordered_page_number', ordered_page_number)
register.filter('filtered_page_number', filtered_page_number)