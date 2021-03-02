import os
import tempfile

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from PIL import Image

from ..models import Recipe
from .base_classes import ViewsTestBase

User = get_user_model()


class RecipesViewsTest(ViewsTestBase):
    def test_template_used(self):
        fd, path = tempfile.mkstemp(suffix='.jpg')
        image = Image.new("RGB", (1, 1), "#000")
        image.save(path)
        recipe = Recipe.objects.create(
            author=self.user, image=path, cooking_time_minutes=60)

        reverse_names_templates = [
            (reverse('recipe_create'), 'recipe_create.html'),
            (reverse('recipe_list'), 'recipe_list.html'),
            (
                reverse('recipe_detail', kwargs={'pk': recipe.id}),
                'recipe_detail.html'
            ),
            (
                reverse('profile', kwargs={'username': self.user.username}),
                'profile.html'
            ),
        ]
        self.check_template_used(reverse_names_templates)

        recipe.delete()
        os.close(fd)
        os.remove(path)
