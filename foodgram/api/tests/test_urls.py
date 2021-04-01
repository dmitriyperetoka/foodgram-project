from django.contrib.auth import get_user_model

from foodgram.tests.base_classes import UrlsTestBase

User = get_user_model()


class ApiUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = ['/api/v1/ingredients/']
        self.check_exists(urls)

    def test_restricted(self):
        urls = [
            '/api/v1/favorites/',
            '/api/v1/purchases/',
            '/api/v1/subscriptions/',
        ]
        self.check_unauthorized_forbidden(urls)
        user = User.objects.create(username='username')
        self.client.force_login(user)
        self.check_get_method_not_allowed(urls)
