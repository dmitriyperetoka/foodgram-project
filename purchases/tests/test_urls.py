from django.conf import settings
from django.contrib.auth import get_user_model

from recipes.tests.base_classes import UrlsTestBase

User = get_user_model()


class PurchasesUrlsTest(UrlsTestBase):
    def test_exists(self):
        user = User.objects.create(username='someuser')
        self.client.force_login(user)
        urls = ['/personal/purchases/new']
        self.check_exists(urls)

    def test_redirects(self):
        redirects = {
            '/personal/purchases/new': f'{settings.LOGIN_URL}?next='
                                       f'/personal/purchases/new',
        }
        self.check_redirects(redirects)
