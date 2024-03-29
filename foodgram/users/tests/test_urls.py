from django.conf import settings
from django.contrib.auth import get_user_model

from foodgram.tests.base_classes import UrlsTestBase

User = get_user_model()


class UsersUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = [
            '/personal/registration/',
            '/personal/auth/login/',
            '/personal/auth/password_reset/',
            '/personal/auth/password_reset/done/',
            '/personal/auth/reset/MQ/set-password/',
            '/personal/auth/reset/done/',
        ]
        self.check_exists(urls)

        user = User.objects.create(username='someuser')
        self.client.force_login(user)
        urls = [
            '/personal/purchases/',
            '/personal/purchases/download/',
            '/personal/favorites/',
            '/personal/subscriptions/',
            '/personal/auth/password_change/',
            '/personal/auth/password_change/done/',

        ]
        self.check_exists(urls)

    def test_redirects(self):
        redirects = {
            '/personal/purchases/download/': f'{settings.LOGIN_URL}?next='
                                             f'/personal/purchases/download/',
            '/personal/purchases/': f'{settings.LOGIN_URL}?next='
                                    f'/personal/purchases/',
        }
        self.check_redirects(redirects)

    def test_redirect_chains(self):
        redirect_chains = {
            '/personal/registration/success/': [('/', 302),
                                                ('/recipes/', 302)],
            '/personal/auth/logout/': [('/', 302), ('/recipes/', 302)],
        }
        self.check_redirect_chains(redirect_chains)
