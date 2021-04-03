import os
import tempfile

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from PIL import Image

from ..models import Recipe
from foodgram.tests.base_classes import ViewsTestBase

User = get_user_model()


class RecipesViewsTest(ViewsTestBase):
    def setUp(self):
        super().setUp()
        self.fd, self.path = tempfile.mkstemp(suffix='.jpg')
        Image.new("RGB", (1, 1), "#000").save(self.path)
        self.recipe = Recipe.objects.create(
            author=self.user, image=self.path, cooking_time_minutes=60)

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    def test_template_used(self):
        reverse_names_templates = [
            (reverse('recipes:recipe_create'), 'recipes/recipe_form.html'),
            (reverse('recipes:recipe_list'), 'recipes/recipe_list.html'),
            (
                reverse(
                    'recipes:author_recipe_list',
                    kwargs={'username': self.user.username}),
                'recipes/recipe_list.html',
            ),
            (
                reverse(
                    'recipes:recipe_detail', kwargs={'pk': self.recipe.id}),
                'recipes/recipe_detail.html',
            ),
            (
                reverse(
                    'recipes:recipe_update', kwargs={'pk': self.recipe.id}),
                'recipes/recipe_form.html'
            ),
            (
                reverse(
                    'recipes:recipe_delete', kwargs={'pk': self.recipe.id}),
                'recipes/recipe_confirm_delete.html'
            ),
        ]
        self.check_template_used(reverse_names_templates)
