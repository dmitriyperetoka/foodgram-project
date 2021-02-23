from django.contrib.auth import get_user_model
from django.db import models, utils

from ..models import PurchaseList, RecipeInPurchaseList
from recipes.models import Recipe
from recipes.tests.base_classes import ModelsTestBase

User = get_user_model()


class PurchasesModelsTest(ModelsTestBase):
    def setUp(self):
        self.author = User.objects.create(username='some_user')
        self.recipe = Recipe.objects.create(
            author=self.author, title='Some Recipe', cooking_time_minutes=60)
        self.purchase_list = PurchaseList.objects.create(
            author=self.author, title='Some Purchase List')
        self.recipe_in_purchase_list = RecipeInPurchaseList.objects.create(
            recipe=self.recipe, purchase_list=self.purchase_list, quantity=2)


class PurchaseListModelTest(PurchasesModelsTest):
    def test_field_list(self):
        field_names = ['id', 'author', 'title']
        self.check_field_list(self.purchase_list, field_names)

    def test_many_to_many_field_list(self):
        field_names = ['recipes']
        self.check_field_list(
            self.purchase_list, field_names, many_to_many=True)

    def test_field_classes(self):
        field_classes = {
            'author': models.ForeignKey,
            'title': models.CharField,
            'recipes': models.ManyToManyField,
        }
        self.check_field_classes(self.purchase_list, field_classes)

    def test_cascade_author(self):
        self.check_cascade(PurchaseList, 'author', User, self.author)

    def test_field_attrs(self):
        field_attr_values = {
            'author': {
                'verbose_name': 'Автор',
                'help_text': 'Автор списка покупок'
            },
            'title': {
                'verbose_name': 'Название',
                'help_text': 'Название списка покупок'
            },
            'recipes': {
                'verbose_name': 'Рецепты',
                'help_text': 'Рецепты, представленные в списке покупок'
            },
        }
        self.check_field_attrs(self.purchase_list, field_attr_values)

    def test_remote_field_attrs(self):
        field_attrs = {
            'recipes': {
                'through': RecipeInPurchaseList,
                'through_fields': ['purchase_list', 'recipe'],
            },
        }
        self.check_field_attrs(self.purchase_list, field_attrs, remote=True)

    def test_related_names(self):
        relations = [
            (self.author, 'purchase_lists'),
            (self.recipe, 'purchase_lists'),
        ]
        self.check_related_names(self.purchase_list, relations)

    def test_model_attrs(self):
        model_attr_values = {
            'verbose_name': 'Список покупок',
            'verbose_name_plural': 'Списки покупок',
        }
        self.check_model_attrs(self.purchase_list, model_attr_values)

    def test_str(self):
        self.assertEqual(
            str(self.purchase_list),
            f'Список покупок #{self.purchase_list.id} '
            f'"{self.purchase_list.title}"')


class ProductSetInPurchaseListModelTest(PurchasesModelsTest):
    def test_field_list(self):
        field_names = ['id', 'purchase_list', 'recipe', 'quantity']
        self.check_field_list(self.recipe_in_purchase_list, field_names)

    def test_field_classes(self):
        field_classes = {
            'purchase_list': models.ForeignKey,
            'recipe': models.ForeignKey,
            'quantity': models.PositiveSmallIntegerField
        }
        self.check_field_classes(self.recipe_in_purchase_list, field_classes)

    def test_purchase_list_cascade(self):
        self.check_cascade(
            RecipeInPurchaseList,
            'purchase_list', PurchaseList, self.purchase_list)

    def test_recipe_cascade(self):
        self.check_cascade(RecipeInPurchaseList, 'recipe', Recipe, self.recipe)

    def test_field_attrs(self):
        field_attr_values = {
            'purchase_list': {
                'verbose_name': 'Список покупок',
                'help_text': 'Список покупок, в котором представлен рецепт',
            },
            'recipe': {
                'verbose_name': 'Рецепт',
                'help_text': 'Рецепт, представленный в списке покупок',
            },
            'quantity': {
                'verbose_name': 'Количество',
                'help_text': 'Количество порций рецепта в списке покупок',
            },
        }
        self.check_field_attrs(self.recipe_in_purchase_list, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'verbose_name': 'Рецепт в списке покупок',
            'verbose_name_plural': 'Рецепты в списках покупок',
        }
        self.check_model_attrs(
            self.recipe_in_purchase_list, model_attr_values)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'purchases_recipeinpurchaselist.purchase_list_id, '
                'purchases_recipeinpurchaselist.recipe_id'
        ):
            RecipeInPurchaseList.objects.create(
                recipe=self.recipe, purchase_list=self.purchase_list,
                quantity=3)

    def test_str(self):
        self.assertEqual(
            str(self.recipe_in_purchase_list),
            f'Рецепт {self.recipe_in_purchase_list.recipe} в списке покупок '
            f'#{self.recipe_in_purchase_list.purchase_list.id}')
