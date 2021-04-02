import os
import tempfile

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from PIL import Image

from ..models import Recipe
from foodgram.tests.base_classes import ViewsTestBase

User = get_user_model()


class RecipesViewsTest(ViewsTestBase):
    def test_template_used(self):
        fd, path = tempfile.mkstemp(suffix='.jpg')
        image = Image.new("RGB", (1, 1), "#000")
        image.save(path)
        recipe = Recipe.objects.create(
            author=self.user, image=path, cooking_time_minutes=60)

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
                reverse('recipes:recipe_detail', kwargs={'pk': recipe.id}),
                'recipes/recipe_detail.html',
            ),
            (
                reverse('recipes:recipe_update', kwargs={'pk': recipe.id}),
                'recipes/recipe_form.html'
            ),
            (
                reverse('recipes:recipe_delete', kwargs={'pk': recipe.id}),
                'recipes/recipe_confirm_delete.html'
            ),
        ]
        self.check_template_used(reverse_names_templates)

        os.close(fd)
        os.remove(path)
