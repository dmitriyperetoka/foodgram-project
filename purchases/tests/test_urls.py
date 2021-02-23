from recipes.tests.base_classes import URLsTestBase


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        urls = ['/purchases/username/1']
        self.check_exists(urls)
