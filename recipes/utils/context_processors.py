from ..models import Tag


def tag_and_colors(request):  # noqa
    colors = ['orange', 'green', 'purple']
    tags = Tag.objects.all()

    return {
        'tags_and_colors': {
            tag: colors[index % len(colors)] for index, tag in enumerate(tags)
        }
    }
