from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class PurchaseList(models.Model):
    """Store purchase lists."""

    author = models.ForeignKey(
        User, models.CASCADE, 'purchase_lists', verbose_name='Автор',
        help_text='Автор списка покупок')
    title = models.CharField(
        'Название', help_text='Название списка покупок', max_length=200)
    recipes = models.ManyToManyField(
        Recipe, 'purchase_lists', through='RecipeInPurchaseList',
        through_fields=['purchase_list', 'recipe'], verbose_name='Рецепты',
        help_text='Рецепты, представленные в списке покупок')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'Список покупок #{self.id} "{self.title}"'


class RecipeInPurchaseList(models.Model):
    """Store the records of how many portions of certain recipes are included
    in certain purchase lists.
    """

    purchase_list = models.ForeignKey(
        PurchaseList, models.CASCADE, verbose_name='Список покупок',
        help_text='Список покупок, в котором представлен рецепт')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, verbose_name='Рецепт',
        help_text='Рецепт, представленный в списке покупок')
    quantity = models.PositiveSmallIntegerField(
        'Количество', help_text='Количество порций рецепта в списке покупок')

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списках покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['purchase_list', 'recipe'],
                name='unique_purchase_list_recipe'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} '
            f'в списке покупок #{self.purchase_list.id}')


class NewPurchaseList(models.Model):
    """Store new purchase lists."""

    author = models.OneToOneField(
        User, models.CASCADE, related_name='new_purchase_list',
        verbose_name='Автор', help_text='Автор нового списка покупок')
    recipes = models.ManyToManyField(
        Recipe, 'new_purchase_lists', through='RecipeInNewPurchaseList',
        through_fields=['new_purchase_list', 'recipe'], verbose_name='Рецепты',
        help_text='Рецепты, представленные в новом списке покупок')

    class Meta:
        verbose_name = 'Новый список покупок'
        verbose_name_plural = 'Новые списки покупок'

    def __str__(self):
        return f'Новый список покупок пользователя {self.author}'


class RecipeInNewPurchaseList(models.Model):
    """Store the records of how many portions of certain recipes are included
    in certain new purchase lists.
    """

    new_purchase_list = models.ForeignKey(
        NewPurchaseList, models.CASCADE, verbose_name='Новый список покупок',
        help_text='Новый список покупок, в котором представлен рецепт')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, verbose_name='Рецепт',
        help_text='Рецепт, представленный в новом списке покупок')
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        help_text='Количество порций рецепта в новом списке покупок',
        default=1)

    class Meta:
        verbose_name = 'Рецепт в новом списке покупок'
        verbose_name_plural = 'Рецепты в новых списках покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['new_purchase_list', 'recipe'],
                name='unique_new_purchase_list_recipe'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} в новом списке покупок '
            f'пользователя {self.new_purchase_list.author}')
