from .base_classes import URLsTestBase


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        urls = ['/recipes/', '/recipes/username', '/recipes/username/1']
        self.check_exists(urls)

    def test_redirects(self):
        redirects = [('/', '/recipes/', 302), ('/recipes', '/recipes/', 301)]
        self.check_redirects(redirects)
