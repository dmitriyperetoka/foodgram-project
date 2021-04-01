from django.shortcuts import reverse

from foodgram.tests.base_classes import ViewsTestBase


class AboutViewsTest(ViewsTestBase):
    def test_template_used(self):
        reverse_names_templates = [
            (reverse('about:project'), 'about/project.html'),
            (reverse('about:tech'), 'about/tech.html')
        ]
        self.check_template_used(reverse_names_templates)
