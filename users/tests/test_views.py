from django.shortcuts import reverse

from recipes.tests.base_classes import ViewsTestBase


class PurchasesViewsTest(ViewsTestBase):
    def test_template_used(self):
        reverse_names_templates = [
            (reverse('login'), 'registration/login.html'),
            (reverse('registration'), 'registration/registration.html'),
            (reverse('favourites'), 'favourites.html'),
            (reverse('subscriptions'), 'subscriptions.html'),
        ]
        self.check_template_used(reverse_names_templates)
