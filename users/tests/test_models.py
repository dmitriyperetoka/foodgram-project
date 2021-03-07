from django.db import models, utils
from django.contrib.auth import get_user_model

from ..models import FavoriteRecipe, Subscription
from recipes.models import Recipe
from recipes.tests.base_classes import ModelsTestBase

User = get_user_model()


class UsersModelsTest(ModelsTestBase):
    def setUp(self):
        self.author = User.objects.create(username='some_user')
        self.user = User.objects.create(username='another_user')


class FavoriteRecipeModelTest(UsersModelsTest):
    def setUp(self):
        super().setUp()
        self.recipe = Recipe.objects.create(
            author=self.author, title='Some Recipe', cooking_time_minutes=60)
        self.favorite_recipe = FavoriteRecipe.objects.create(
            user=self.user, recipe=self.recipe)

    def test_field_list(self):
        field_names = ['id', 'user', 'recipe']
        self.check_field_list(self.favorite_recipe, field_names)

    def test_field_classes(self):
        field_classes = {
            'user': models.ForeignKey,
            'recipe': models.ForeignKey,
        }
        self.check_field_classes(self.favorite_recipe, field_classes)

    def test_cascade_author(self):
        self.check_cascade(FavoriteRecipe, 'user', User, self.user)

    def test_cascade_recipe(self):
        self.check_cascade(FavoriteRecipe, 'recipe', Recipe, self.recipe)

    def test_related_names(self):
        relations = [
            (self.user, 'favorite_recipes'),
            (self.recipe, 'favorite_lists'),
        ]
        self.check_related_names(self.favorite_recipe, relations)

    def test_field_attrs(self):
        field_attr_values = {
            'user': {
                'related_model': User,
                'verbose_name': 'Пользователь',
                'help_text': 'Пользователь, '
                             'который добавил рецепт в список избранного'
            },
            'recipe': {
                'related_model': Recipe,
                'verbose_name': 'Рецепт',
                'help_text': 'Рецепт, '
                             'который пользователь добавил в список избранного'
            },
        }
        self.check_field_attrs(self.favorite_recipe, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'verbose_name': 'Рецепт в списке избранного',
            'verbose_name_plural': 'Рецепты в списках избранного',
        }
        self.check_model_attrs(self.favorite_recipe, model_attr_values)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_favoriterecipe.user_id, '
                'users_favoriterecipe.recipe_id'
        ):
            FavoriteRecipe.objects.create(
                user=self.user, recipe=self.recipe)

    def test_str(self):
        self.assertEqual(
            str(self.favorite_recipe),
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')


class SubscriptionModelTest(UsersModelsTest):
    def setUp(self):
        super().setUp()
        self.subscription = Subscription.objects.create(
            subscriber=self.user, author=self.author)

    def test_field_list(self):
        field_names = ['id', 'subscriber', 'author']
        self.check_field_list(self.subscription, field_names)

    def test_field_classes(self):
        field_classes = {
            'subscriber': models.ForeignKey,
            'author': models.ForeignKey,
        }
        self.check_field_classes(self.subscription, field_classes)

    def test_cascade_subscriber(self):
        self.check_cascade(Subscription, 'subscriber', User, self.user)

    def test_cascade_author(self):
        self.check_cascade(Subscription, 'author', User, self.author)

    def test_related_names(self):
        relations = [
            (self.user, 'favorite_authors'),
            (self.author, 'subscribers'),
        ]
        self.check_related_names(self.subscription, relations)

    def test_field_attrs(self):
        field_attrs = {
            'subscriber': {
                'related_model': User,
                'verbose_name': 'Подписчик',
                'help_text': 'Пользователь, который подписан '
                             'на автора публикаций',
            },
            'author': {
                'related_model': User,
                'verbose_name': 'Автор',
                'help_text': 'Автор публикаций, '
                             'на которого подписан пользователь',
            },
        }
        self.check_field_attrs(self.subscription, field_attrs)

    def test_model_attrs(self):
        model_attrs = {
            'verbose_name': 'Подписка',
            'verbose_name_plural': 'Подписки',
        }
        self.check_model_attrs(self.subscription, model_attrs)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_subscription.subscriber_id, '
                'users_subscription.author_id'
        ):
            Subscription.objects.create(
                subscriber=self.user, author=self.author)

    def test_not_self_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'CHECK constraint failed: subscriber_not_author'
        ):
            Subscription.objects.create(
                subscriber=self.user, author=self.user)

    def test_str(self):
        self.assertEqual(
            str(self.subscription),
            f'{self.subscription.subscriber} '
            f'подписан(а) на {self.subscription.author}')
