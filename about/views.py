from django.views.generic.base import TemplateView


class AboutProjectView(TemplateView):
    template_name = 'about/project.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    extra_context = {
        'tech': [
            ('Python', '3.9.2', 'https://www.python.org/'),
            ('Django Framework', '3.1.6', 'https://www.djangoproject.com/'),
            (
                'Django REST Framework', '3.12.2',
                'https://www.django-rest-framework.org/'
            ),
            ('Pillow', '8.1.1', 'https://python-pillow.org/'),
            ('Gunicorn', None, 'https://gunicorn.org/'),
            ('PostgreSQL', None, 'https://www.postgresql.org/'),
            ('Nginx', None, 'https://nginx.org/'),
            ('Docker', None, 'https://www.docker.com/'),
        ]
    }
