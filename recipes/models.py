from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Store tags that recipes can be filtered by."""

    title = models.CharField(
        'Название', help_text='Название тэга',
        max_length=60, unique=True)
    slug = models.SlugField('Slug', help_text='Slug тэга', unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Store ingredients that can be included in recipes."""

    title = models.CharField(
        'Название', help_text='Название ингредиента', max_length=200)
    dimension_unit = models.CharField(
        'Единица измерения', help_text='Единица измерения ингредиента',
        max_length=20)

    class Meta:
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
        'Время готовки', help_text='Время готовки в минутах')
    pub_date = models.DateTimeField(
        'Дата публикации', help_text='Определяется автоматически',
        auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'#{self.id} "{self.title}"'


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
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.title} {self.quantity} '
            f'{self.ingredient.dimension_unit} '
            f'в рецепте {self.recipe}')


class FavouriteRecipe(models.Model):
    """Store the records that certain recipes are in the favourite lists
    of certain users.
    """

    user = models.ForeignKey(
        User, models.CASCADE, 'favourite_recipes', verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в список избранного')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, 'favourite_lists', verbose_name='Рецепт',
        help_text='Рецепт, который пользователь добавил в список избранного')

    class Meta:
        verbose_name = 'Рецепт в списке избранного'
        verbose_name_plural = 'Рецепты в списках избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favourite_recipe'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')
