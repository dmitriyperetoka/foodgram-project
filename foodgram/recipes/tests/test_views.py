import os
import tempfile

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from PIL import Image

from ..models import Recipe, Tag
from foodgram import settings
from foodgram.tests.base_classes import ViewsTestBase

User = get_user_model()


class RecipesViewsTest(ViewsTestBase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.client.force_login(self.user)
        self.another_user = User.objects.create(username='anotheruser')
        self.users = User.objects.all()

        tags = [
            Tag(title='Завтрак', slug='breakfast'),
            Tag(title='Обед', slug='lunch'),
            Tag(title='Ужин', slug='dinner'),
        ]
        Tag.objects.bulk_create(tags)
        self.tags = Tag.objects.all()

        self.fd, self.path = tempfile.mkstemp(suffix='.jpg')
        Image.new("RGB", (1, 1), "#000").save(self.path)

        self.recipe_kwargs = {
            'author': self.user, 'image': self.path,
            'title': 'Just some title', 'description': 'Just some description',
            'cooking_time_minutes': 60}
        self.recipe = Recipe.objects.create(**self.recipe_kwargs)

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
                'recipes/recipe_form.html',
            ),
            (
                reverse(
                    'recipes:recipe_delete', kwargs={'pk': self.recipe.id}),
                'recipes/recipe_confirm_delete.html',
            ),
        ]
        self.check_template_used(reverse_names_templates)

    def test_object_list_in_context(self):
        recipes = []
        for q in range(19):
            self.recipe_kwargs.update(
                {'author': self.users[q % len(self.users)]})
            recipes.append(Recipe(**self.recipe_kwargs))
        Recipe.objects.bulk_create(recipes)

        for index, recipe in enumerate(Recipe.objects.all()):
            recipe.tags.set([self.tags[index % len(self.tags)]])

        queryset = Recipe.objects.all()
        author_queryset = queryset.filter(
            author__username=self.another_user.username)

        start_index = 0
        stop_index = settings.PAGINATE_BY

        pages = [
            [
                reverse('recipes:recipe_list'),
                queryset, [start_index, stop_index],
            ],
            [
                reverse(
                    'recipes:author_recipe_list',
                    kwargs={'username': self.another_user.username}),
                author_queryset, [start_index, stop_index],
            ],
        ]
        self.check_object_list_in_context(pages)

        for page in pages:
            page[0] += f'?tags={self.tags[0].slug}'
            page[1].filter(tags__slug__in=[self.tags[0].slug])
        self.check_object_list_in_context(pages)

        start_index += settings.PAGINATE_BY
        stop_index += settings.PAGINATE_BY
        for page in pages:
            page[0] += '&page=2'
            page[2][0], page[2][1] = start_index, stop_index
        self.check_object_list_in_context(pages)

    def test_extra_context_passed(self):
        pages = [
            (
                reverse(
                    'recipes:author_recipe_list',
                    kwargs={'username': self.another_user.username}),
                {'author': self.another_user},
            ),
        ]
        self.check_extra_context_passed(pages)
