from django import template

register = template.Library()


@register.filter('dict_lookup')
def dict_lookup(dict_, key):
    """Lookup a value in a dictionary by key."""
    return dict_[key]


@register.filter('list_lookup')
def list_lookup(list_, index):
    """Lookup a value in a list by index."""
    return list_[index]


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


@register.filter('get_slice_range')
def get_slice_range(num_pages, page_number):
    if num_pages <= 9:
        return ':9'

    if page_number <= 5:
        return ':7'

    if page_number > num_pages - 5:
        return '-7:'

    return f'{page_number - 3}:{page_number + 2}'
