from recipes.tests.base_classes import URLsTestBase


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        urls = ['/users/favourites/username', '/users/subscriptions/username']
        self.check_exists(urls)
