from .base_classes import URLsTestBase


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        urls = ['/', '/username', '/username/1', '/username/favourites']
        self.check_exists(urls)
