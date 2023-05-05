from django import template
import re

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

register.filter('loop_by_number', loop_by_number)
register.filter('ordering_value', ordering_value)