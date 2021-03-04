from django import template

register = template.Library()


@register.filter('dict_lookup')
def dict_lookup(dictionary, key):
    """Lookup a value in a dictionary by key."""
    return dictionary[key]


@register.filter('make_url_tags_query')
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


@register.filter('parse_url_tags_query')
def parse_url_tags_query(request):
    """Parse url to get tags for filtering."""
    return request.GET.getlist('tags')
