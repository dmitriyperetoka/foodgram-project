from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..models import Recipe
from foodgram import settings
from foodgram.tests.base_classes import RecipesViewsSetupBase, ViewsTestBase

User = get_user_model()


class RecipesViewsTest(ViewsTestBase, RecipesViewsSetupBase):
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

    def test_object_in_context(self):
        pages = [
            (
                reverse(
                    'recipes:recipe_detail', kwargs={'pk': self.recipe.id}),
                self.recipe,
            ),
            (
                reverse(
                    'recipes:recipe_update', kwargs={'pk': self.recipe.id}),
                self.recipe,
            ),
            (
                reverse(
                    'recipes:recipe_delete', kwargs={'pk': self.recipe.id}),
                self.recipe,
            ),
        ]
        self.check_object_in_context(pages)

    def test_object_list_in_context(self):
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
            page[1] = page[1].filter(tags__slug__in=[self.tags[0].slug])
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
