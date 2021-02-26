from django.contrib.auth import get_user_model

from .base_classes import URLsTestBase

User = get_user_model()


class RecipeURLsTest(URLsTestBase):
    def test_exists(self):
        author = User.objects.create(username='someuser')
        # add recipe_detail url test when create recipe form is implemented
        urls = ['/recipes/', f'/recipes/author/{author.username}']
        self.check_exists(urls)

    def test_redirects(self):
        redirects = [('/', '/recipes/', 302), ('/recipes', '/recipes/', 301)]
        self.check_redirects(redirects)
