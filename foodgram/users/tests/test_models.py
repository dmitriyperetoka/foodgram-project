from django.db import models, utils
from django.contrib.auth import get_user_model

from ..models import Favorite, Purchase, Subscription
from recipes.models import Recipe
from foodgram.tests.base_classes import ModelsTestBase

User = get_user_model()


class UsersModelsTest(ModelsTestBase):
    def setUp(self):
        self.author = User.objects.create(username='some_user')
        self.user = User.objects.create(username='another_user')

    def get_recipe(self):
        return Recipe.objects.create(
            author=self.author, title='Some Recipe', cooking_time_minutes=60)


class PurchaseModelTest(UsersModelsTest):
    def setUp(self):
        super().setUp()
        self.recipe = self.get_recipe()
        self.purchase = Purchase.objects.create(
            user=self.user, recipe=self.recipe)

    def test_field_list(self):
        field_names = ['id', 'user', 'recipe']
        self.check_field_list(self.purchase, field_names)

    def test_field_classes(self):
        field_classes = {
            'user': models.ForeignKey,
            'recipe': models.ForeignKey,
        }
        self.check_field_classes(self.purchase, field_classes)

    def test_cascade_author(self):
        self.check_cascade(Purchase, 'user', User, self.user)

    def test_cascade_recipe(self):
        self.check_cascade(Purchase, 'recipe', Recipe, self.recipe)

    def test_related_names(self):
        relations = [
            (self.user, 'purchases'),
            (self.recipe, 'purchase_lists'),
        ]
        self.check_related_names(self.purchase, relations)

    def test_field_attrs(self):
        field_attr_values = {
            'user': {
                'related_model': User,
                'verbose_name': 'Пользователь',
                'help_text': 'Пользователь, '
                             'который добавил рецепт в список покупок'
            },
            'recipe': {
                'related_model': Recipe,
                'verbose_name': 'Рецепт',
                'help_text': 'Рецепт, '
                             'представленный в списке покупок пользователя',
            },
        }
        self.check_field_attrs(self.purchase, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'ordering': ['-recipe__pub_date'],
            'verbose_name': 'Рецепт в списке покупок',
            'verbose_name_plural': 'Рецепты в списках покупок',
        }
        self.check_model_attrs(self.purchase, model_attr_values)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_purchase.user_id, '
                'users_purchase.recipe_id'
        ):
            Purchase.objects.create(
                user=self.user, recipe=self.recipe)

    def test_str(self):
        self.assertEqual(
            str(self.purchase),
            f'Рецепт {self.recipe} '
            f'в списке покупок у пользователя {self.user}')


class FavoriteModelTest(UsersModelsTest):
    def setUp(self):
        super().setUp()
        self.recipe = self.get_recipe()
        self.favorite = Favorite.objects.create(
            user=self.user, recipe=self.recipe)

    def test_field_list(self):
        field_names = ['id', 'user', 'recipe']
        self.check_field_list(self.favorite, field_names)

    def test_field_classes(self):
        field_classes = {
            'user': models.ForeignKey,
            'recipe': models.ForeignKey,
        }
        self.check_field_classes(self.favorite, field_classes)

    def test_cascade_author(self):
        self.check_cascade(Favorite, 'user', User, self.user)

    def test_cascade_recipe(self):
        self.check_cascade(Favorite, 'recipe', Recipe, self.recipe)

    def test_related_names(self):
        relations = [
            (self.user, 'favorites'),
            (self.recipe, 'favorite_lists'),
        ]
        self.check_related_names(self.favorite, relations)

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
        self.check_field_attrs(self.favorite, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'ordering': ['-recipe__pub_date'],
            'verbose_name': 'Рецепт в списке избранного',
            'verbose_name_plural': 'Рецепты в списках избранного',
        }
        self.check_model_attrs(self.favorite, model_attr_values)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_favorite.user_id, '
                'users_favorite.recipe_id'
        ):
            Favorite.objects.create(
                user=self.user, recipe=self.recipe)

    def test_str(self):
        self.assertEqual(
            str(self.favorite),
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')


class SubscriptionModelTest(UsersModelsTest):
    def setUp(self):
        super().setUp()
        self.subscription = Subscription.objects.create(
            user=self.user, author=self.author)

    def test_field_list(self):
        field_names = ['id', 'user', 'author']
        self.check_field_list(self.subscription, field_names)

    def test_field_classes(self):
        field_classes = {
            'user': models.ForeignKey,
            'author': models.ForeignKey,
        }
        self.check_field_classes(self.subscription, field_classes)

    def test_cascade_user(self):
        self.check_cascade(Subscription, 'user', User, self.user)

    def test_cascade_author(self):
        self.check_cascade(Subscription, 'author', User, self.author)

    def test_related_names(self):
        relations = [
            (self.user, 'subscriptions'),
            (self.author, 'subscribers'),
        ]
        self.check_related_names(self.subscription, relations)

    def test_field_attrs(self):
        field_attrs = {
            'user': {
                'related_model': User,
                'verbose_name': 'Пользователь',
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
            'ordering': ['author__first_name', 'author__last_name'],
            'verbose_name': 'Подписка',
            'verbose_name_plural': 'Подписки',
        }
        self.check_model_attrs(self.subscription, model_attrs)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_subscription.user_id, '
                'users_subscription.author_id'
        ):
            Subscription.objects.create(
                user=self.user, author=self.author)

    def test_not_self_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'CHECK constraint failed: user_not_author'
        ):
            Subscription.objects.create(
                user=self.user, author=self.user)

    def test_str(self):
        self.assertEqual(
            str(self.subscription),
            f'{self.subscription.user} '
            f'подписан(а) на {self.subscription.author}')
