from django.contrib.auth import get_user_model
from django.db import models, utils

from ..models import (
    FavouriteRecipe, Ingredient, IngredientInRecipe, Recipe, Tag,
)
from .base_classes import ModelsTestBase

User = get_user_model()


class RecipesModelsTest(ModelsTestBase):
    def setUp(self):
        self.author = User.objects.create(username='some_user')
        self.recipe = Recipe.objects.create(
            author=self.author, title='Some Recipe', cooking_time_minutes=60)


class FavouriteRecipeModelTest(RecipesModelsTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='another_user')
        self.favorite_recipe = FavouriteRecipe.objects.create(
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
        self.check_cascade(FavouriteRecipe, 'user', User, self.user)

    def test_cascade_recipe(self):
        self.check_cascade(FavouriteRecipe, 'recipe', Recipe, self.recipe)

    def test_related_names(self):
        relations = [
            (self.user, 'favourite_recipes'),
            (self.recipe, 'favourite_lists'),
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
                'recipes_favouriterecipe.user_id, '
                'recipes_favouriterecipe.recipe_id'
        ):
            FavouriteRecipe.objects.create(
                user=self.user, recipe=self.recipe)

    def test_str(self):
        self.assertEqual(
            str(self.favorite_recipe),
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')


class IngredientInRecipeModelTest(RecipesModelsTest):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.objects.create(
            title='Some Ingredient', dimension_unit='g')
        self.ingredient_in_recipe = IngredientInRecipe.objects.create(
            ingredient=self.ingredient, recipe=self.recipe, quantity=3)

    def test_field_list(self):
        field_names = ['id', 'recipe', 'ingredient', 'quantity']
        self.check_field_list(self.ingredient_in_recipe, field_names)

    def test_field_classes(self):
        field_classes = {
            'recipe': models.ForeignKey,
            'ingredient': models.ForeignKey,
            'quantity': models.PositiveSmallIntegerField
        }
        self.check_field_classes(self.ingredient_in_recipe, field_classes)

    def test_recipe_cascade(self):
        self.check_cascade(IngredientInRecipe, 'recipe', Recipe, self.recipe)

    def test_ingredient_cascade(self):
        self.check_cascade(
            IngredientInRecipe, 'ingredient', Ingredient, self.ingredient)

    def test_field_attrs(self):
        field_attr_values = {
            'recipe': {
                'related_model': Recipe,
                'verbose_name': 'Рецепт',
                'help_text': 'Рецепт, в котором представлен нигредиент',
            },
            'ingredient': {
                'related_model': Ingredient,
                'verbose_name': 'Ингредиент',
                'help_text': 'Ингредиент, представленный в рецепте',
            },
            'quantity': {
                'verbose_name': 'Количество',
                'help_text': 'Количество ингредиента в рецепте',
            },
        }
        self.check_field_attrs(self.ingredient_in_recipe, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'verbose_name': 'Ингредиент в рецепте',
            'verbose_name_plural': 'Ингредиенты в рецептах',
        }
        self.check_model_attrs(
            self.ingredient_in_recipe, model_attr_values)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'recipes_ingredientinrecipe.recipe_id, '
                'recipes_ingredientinrecipe.ingredient_id'
        ):
            IngredientInRecipe.objects.create(
                ingredient=self.ingredient, recipe=self.recipe, quantity=2)

    def test_str(self):
        self.assertEqual(
            str(self.ingredient_in_recipe),
            f'{self.ingredient_in_recipe.ingredient.title} '
            f'{self.ingredient_in_recipe.quantity} '
            f'{self.ingredient_in_recipe.ingredient.dimension_unit} '
            f'в рецепте {self.ingredient_in_recipe.recipe}')


class RecipeModelTest(RecipesModelsTest):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.objects.create(
            title='Some Ingredient', dimension_unit='g')
        self.ingredient_in_recipe = IngredientInRecipe.objects.create(
            ingredient=self.ingredient, recipe=self.recipe, quantity=3)
        self.tag = Tag.objects.create(title='Tag')
        self.recipe.tags.add(self.tag)

    def test_field_list(self):
        field_names = [
            'id', 'author',  'title', 'description', 'image',
            'cooking_time_minutes', 'pub_date',
        ]
        self.check_field_list(self.recipe, field_names)

    def test_many_to_many_field_list(self):
        field_names = ['ingredients', 'tags']
        self.check_field_list(self.recipe, field_names, many_to_many=True)

    def test_field_classes(self):
        field_classes = {
            'author': models.ForeignKey,
            'title': models.CharField,
            'description': models.TextField,
            'image': models.ImageField,
            'cooking_time_minutes': models.PositiveSmallIntegerField,
            'pub_date': models.DateTimeField,
        }
        self.check_field_classes(self.recipe, field_classes)

    def test_cascade_author(self):
        self.check_cascade(Recipe, 'author', User, self.author)

    def test_related_names(self):
        relations = [
            (self.author, 'recipes'),
            (self.ingredient, 'recipes'),
            (self.tag, 'recipes'),
        ]
        self.check_related_names(self.recipe, relations)

    def test_field_attrs(self):
        field_attrs = {
            'author': {
                'verbose_name': 'Автор',
                'help_text': 'Автор рецепта',
            },
            'title': {
                'verbose_name': 'Название',
                'help_text': 'Название рецепта',
                'max_length': 200,
            },
            'description': {
                'verbose_name': 'Описание',
                'help_text': 'Описание рецепта',
                'max_length': 2000,
            },
            'image': {
                'verbose_name': 'Изображение',
                'help_text': 'Изображение готового блюда',
                'upload_to': 'recipes/'
            },
            'ingredients': {
                'related_model': Ingredient,
                'verbose_name': 'Ингредиенты',
                'help_text': 'Список ингредиентов, представленных в рецепте',
            },
            'tags': {
                'related_model': Tag,
                'verbose_name': 'Тэги',
                'help_text': 'Тэги рецепта',
            },
            'cooking_time_minutes': {
                'verbose_name': 'Время готовки',
                'help_text': 'Время готовки в минутах',
            },
            'pub_date': {
                'verbose_name': 'Дата публикации',
                'help_text': 'Определяется автоматически',
                'auto_now_add': True,
                'db_index': True,
            },
        }
        self.check_field_attrs(self.recipe, field_attrs)

    def test_remote_field_attrs(self):
        field_attrs = {
            'ingredients': {
                'through': IngredientInRecipe,
                'through_fields': ['recipe', 'ingredient'],
            },
        }
        self.check_field_attrs(self.recipe, field_attrs, remote=True)

    def test_model_attrs(self):
        model_attr_values = {
            'ordering': ['-pub_date'],
            'verbose_name': 'Рецепт',
            'verbose_name_plural': 'Рецепты',
        }
        self.check_model_attrs(self.recipe, model_attr_values)

    def test_str(self):
        self.assertEqual(
            str(self.recipe),
            f'#{self.recipe.id} "{self.recipe.title}"')


class TagModelTest(RecipesModelsTest):
    def setUp(self):
        self.tag = Tag.objects.create(title='Tag', slug='slug')

    def test_field_list(self):
        field_names = ['id', 'title', 'slug']
        self.check_field_list(self.tag, field_names)

    def test_field_classes(self):
        field_classes = {'title': models.CharField, 'slug': models.SlugField}
        self.check_field_classes(self.tag, field_classes)

    def test_field_attrs(self):
        field_attrs = {
            'title': {
                'verbose_name': 'Название',
                'help_text': 'Название тэга',
                'max_length': 60,
                'unique': True,
            },
            'slug': {
                'verbose_name': 'Slug',
                'help_text': 'Slug тэга',
                'unique': True,
            }
        }
        self.check_field_attrs(self.tag, field_attrs)

    def test_model_attrs(self):
        model_attrs = {'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'}
        self.check_model_attrs(self.tag, model_attrs)

    def test_title_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: recipes_tag.title'
        ):
            Tag.objects.create(title='Tag', slug='slug_')

    def test_slug_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: recipes_tag.slug'
        ):
            Tag.objects.create(title='Tag_', slug='slug')

    def test_str(self):
        self.assertEqual(str(self.tag), self.tag.title)


class IngredientModelTest(RecipesModelsTest):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            title='Some Ingredient', dimension_unit='g')

    def test_field_list(self):
        field_names = ['id', 'title', 'dimension_unit']
        self.check_field_list(self.ingredient, field_names)

    def test_field_classes(self):
        field_classes = {
            'title': models.CharField,
            'dimension_unit': models.CharField,
        }
        self.check_field_classes(self.ingredient, field_classes)

    def test_field_attrs(self):
        field_attr_values = {
            'title': {
                'verbose_name': 'Название',
                'help_text': 'Название ингредиента',
                'max_length': 200,
            },
            'dimension_unit': {
                'verbose_name': 'Единица измерения',
                'help_text': 'Единица измерения ингредиента',
                'max_length': 20,
            },
        }
        self.check_field_attrs(self.ingredient, field_attr_values)

    def test_model_attrs(self):
        model_attr_values = {
            'verbose_name': 'Ингредиент',
            'verbose_name_plural': 'Ингредиенты',
        }
        self.check_model_attrs(self.ingredient, model_attr_values)

    def test_str(self):
        self.assertEqual(
            str(self.ingredient),
            f'{self.ingredient.title}, {self.ingredient.dimension_unit}')
