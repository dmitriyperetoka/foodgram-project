from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

User = get_user_model()


class Tag(models.Model):
    """Store tags that recipes can be filtered by."""

    title = models.CharField(
        'Название', help_text='Название тега', max_length=60, unique=True)
    slug = models.SlugField('Slug', help_text='Slug тега', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Store ingredients that can be included in recipes."""

    title = models.CharField(
        'Название', help_text='Название ингредиента', max_length=200,
        unique=True)
    dimension_unit = models.CharField(
        'Единица измерения', help_text='Единица измерения ингредиента',
        max_length=20)

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension_unit}'


class Recipe(models.Model):
    """Store recipes."""
    author = models.ForeignKey(
        User, models.CASCADE,
        'recipes', verbose_name='Автор', help_text='Автор рецепта')
    title = models.CharField(
        'Название', help_text='Название рецепта', max_length=200)
    description = models.TextField(
        'Описание', help_text='Описание рецепта', max_length=2000)
    image = models.ImageField(
        'Изображение', help_text='Изображение готового блюда',
        upload_to='recipes/')
    ingredients = models.ManyToManyField(
        Ingredient, 'recipes', verbose_name='Ингредиенты',
        help_text='Список ингредиентов, представленных в рецепте',
        through='IngredientInRecipe', through_fields=['recipe', 'ingredient'])
    tags = models.ManyToManyField(
        Tag, 'recipes', verbose_name='Тэги', help_text='Тэги рецепта')
    cooking_time_minutes = models.PositiveSmallIntegerField(
        'Время приготовления', help_text='Время приготовления в минутах')
    pub_date = models.DateTimeField(
        'Дата публикации', help_text='Определяется автоматически',
        auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'#{self.id} "{self.title}"'

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.id})


class IngredientInRecipe(models.Model):
    """Store the records of which quantity of certain ingredients
    are included certain recipes.
    """

    recipe = models.ForeignKey(
        Recipe, models.CASCADE, verbose_name='Рецепт',
        help_text='Рецепт, в котором представлен нигредиент')
    ingredient = models.ForeignKey(
        Ingredient, models.CASCADE, verbose_name='Ингредиент',
        help_text='Ингредиент, представленный в рецепте')
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиента в рецепте')

    class Meta:
        ordering = ['ingredient__title']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.title} {self.quantity} '
            f'{self.ingredient.dimension_unit} '
            f'в рецепте {self.recipe}')
