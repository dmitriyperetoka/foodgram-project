from django.views.generic.base import TemplateView


class AboutProjectView(TemplateView):
    """Display about project page."""

    template_name = 'about/project.html'


class AboutTechView(TemplateView):
    """Display about technologies page."""

    template_name = 'about/tech.html'
    extra_context: dict[str, list[tuple[str, str, str]]] = {
        'tech': [
            ('Python', '3.9.2', 'https://www.python.org/'),
            ('Django Framework', '3.1.6', 'https://www.djangoproject.com/'),
            (
                'Django REST Framework', '3.12.2',
                'https://www.django-rest-framework.org/'
            ),
            ('Pillow', '8.1.1', 'https://python-pillow.org/'),
            ('Gunicorn', '20.0.4', 'https://gunicorn.org/'),
            ('PostgreSQL', '12.5', 'https://www.postgresql.org/'),
            ('Nginx', '1.18', 'https://nginx.org/'),
            ('Docker', '20.10.5', 'https://www.docker.com/'),
        ]
    }
