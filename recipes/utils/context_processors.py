from ..models import Recipe, Tag


def tag_and_colors(request):  # noqa
    colors = ['orange', 'green', 'purple']
    tags = Tag.objects.all()

    return {
        'tags_and_colors': {
            tag: colors[index % len(colors)] for index, tag in enumerate(tags)
        }
    }


def request_user_favourites(request):
    return {
        'request_user_favourites':
            Recipe.objects.filter(favourite_lists__user=request.user)
    }
