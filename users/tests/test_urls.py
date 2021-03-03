from django.contrib.auth import get_user_model

from recipes.tests.base_classes import UrlsTestBase

User = get_user_model()


class UsersUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = [
            '/personal/registration',
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
            '/personal/favourites',
            '/personal/subscriptions',
            '/personal/auth/password_change/',
            '/personal/auth/password_change/done/',

        ]
        self.check_exists(urls)

    def test_redirects(self):
        redirects = {'/personal/auth/logout/': '/recipes/'}
        self.check_redirects(redirects)
