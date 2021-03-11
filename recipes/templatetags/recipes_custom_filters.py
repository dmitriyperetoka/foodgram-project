from django import template
from django.contrib.auth import get_user_model

from ..models import Recipe, Tag

User = get_user_model()

register = template.Library()


@register.filter
def dict_lookup(dict_, key):
    """Lookup a value in a dictionary by key."""
    return dict_[key]


@register.filter
def dict_items(dict_):
    """Lookup a value in a dictionary by key."""
    return dict_.items()


@register.filter
def list_lookup(list_, index):
    """Lookup a value in a list by index."""
    return list_[index]


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
def request_user_favorites(request, recipe):
    return recipe in Recipe.objects.filter(favorite_lists__user=request.user)


@register.filter
def request_user_purchases(request, recipe):
    return recipe in Recipe.objects.filter(
        purchase_lists__user=request.user)


@register.filter
def request_user_subscriptions(request, author):
    return author in User.objects.filter(subscribers__subscriber=request.user)
