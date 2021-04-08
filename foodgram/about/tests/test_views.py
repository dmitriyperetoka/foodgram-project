from django.shortcuts import reverse

from foodgram.tests.base_classes import ViewsTestBase


class AboutViewsTest(ViewsTestBase):
    def test_template_used(self):
        reverse_names_templates = [
            (reverse('about:project'), 'about/project.html'),
            (reverse('about:tech'), 'about/tech.html')
        ]
        self.check_template_used(reverse_names_templates)

    def test_extra_context_passed(self):
        about_tech_extra_context = {
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
        pages = [(reverse('about:tech'), about_tech_extra_context)]
        self.check_extra_context_passed(pages)
