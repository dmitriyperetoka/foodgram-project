from django import template
from django.contrib.auth import get_user_model

from ..models import Recipe, Tag

User = get_user_model()

register = template.Library()

RECIPE_WORD_FORMS = {'one': 'рецепт', 'few': 'рецепта', 'many': 'рецептов'}
RECIPES_PER_CARD = 3


def select_word_form(quantity, forms):
    ten_remainder = quantity % 10
    hundred_remainder = quantity % 100

    if (
            ten_remainder == 0
            or ten_remainder >= 5
            or hundred_remainder in range(11, 15)
    ):
        return forms['many']

    if ten_remainder == 1:
        return forms['one']

    return forms['few']


@register.filter
def get_extra_recipes_message(quantity):
    if quantity <= RECIPES_PER_CARD:
        return

    extra_quantity = quantity - RECIPES_PER_CARD
    word_form = select_word_form(extra_quantity, RECIPE_WORD_FORMS)
    return f'Ещё {extra_quantity} {word_form}...'


@register.filter
def make_url_tags_query(request, slug):
    """Make url for filtering by tags."""
    get = request.GET.copy()
    get.setlist('page', [])
    slugs = get.getlist('tags')

    if slug in slugs:
        slugs.remove(slug)
    else:
        slugs.append(slug)

    get.setlist('tags', slugs)
    return get.urlencode()


@register.filter
def parse_url_tags_query(request):
    """Parse url to get tags for filtering."""
    return request.GET.getlist('tags')


@register.filter
def get_slice_range(num_pages, page_number):
    if num_pages <= 9:
        return ':9'

    if page_number <= 5:
        return ':7'

    if page_number > num_pages - 5:
        return '-7:'

    return f'{page_number - 3}:{page_number + 2}'


@register.filter
def tags_and_colors(request):  # noqa
    colors = ['orange', 'green', 'purple']
    tags = Tag.objects.all()
    return {tag: colors[index % len(colors)] for index, tag in enumerate(tags)}


@register.filter
def dict_items(dict_):
    """Get dictionary items."""
    return dict_.items()


@register.filter
def dict_lookup(dict_, key):
    """Lookup a value in a dictionary by key."""
    return dict_[key]


@register.filter
def list_lookup(list_, index):
    """Lookup a value in a list by index."""
    return list_[index]


@register.filter()
def add_class(field, class_):
    """Add class to a form field."""
    return field.as_widget(attrs={'class': class_})
