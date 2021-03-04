from django import template

register = template.Library()


@register.filter('dict_lookup')
def dict_lookup(dictionary, key):
    """Lookup a value in a dictionary by key."""
    return dictionary[key]
