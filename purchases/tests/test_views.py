from django.shortcuts import reverse

from recipes.tests.base_classes import ViewsTestBase


class PurchasesViewsTest(ViewsTestBase):
    def test_template_used(self):
        reverse_names_templates = [
            (reverse('new_purchase_list'), 'purchases/purchase_list.html'),
        ]
        self.check_template_used(reverse_names_templates)
