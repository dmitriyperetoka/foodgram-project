from django.contrib.auth import get_user_model

from recipes.tests.base_classes import UrlsTestBase

User = get_user_model()


class UsersUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = ['/personal/registration', '/personal/auth/login/']
        self.check_exists(urls)

        user = User.objects.create(username='someuser')
        self.client.force_login(user)
        urls = ['/personal/favourites', '/personal/subscriptions']
        self.check_exists(urls)

    def test_redirects(self):
        redirects = {'/personal/auth/logout/': '/recipes/'}
        self.check_redirects(redirects)
