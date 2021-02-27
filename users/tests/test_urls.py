from recipes.tests.base_classes import URLsTestBase


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        urls = ['/personal/favourites', '/personal/subscriptions']
        self.check_exists(urls)