import os
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image

from ..models import Recipe
from foodgram.tests.base_classes import UrlsTestBase

User = get_user_model()


class RecipesUrlsTest(UrlsTestBase):
    def test_exists(self):
        author = User.objects.create(username='someuser')
        fd, path = tempfile.mkstemp(suffix='.jpg')
        image = Image.new("RGB", (1, 1), "#000")
        image.save(path)
        recipe = Recipe.objects.create(
            author=author, image=path, cooking_time_minutes=60)

        urls = [
            '/recipes/',
            f'/recipes/author/{author.username}',
            f'/recipes/id/{recipe.id}',
        ]

        self.check_exists(urls)
        recipe.delete()
        os.close(fd)
        os.remove(path)

        self.client.force_login(author)
        urls = ['/recipes/new']
        self.check_exists(urls)

    def test_redirects(self):
        redirects = {
            '/': '/recipes/',
            '/recipes/new': f'{settings.LOGIN_URL}?next=/recipes/new',
        }
        self.check_redirects(redirects)
