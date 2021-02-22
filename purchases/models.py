from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class PurchaseList(models.Model):
    """Store purchase lists."""

    author = models.ForeignKey(
        User, models.CASCADE, 'purchase_lists', verbose_name='Автор',
        help_text='Автор списка покупок')
    recipes = models.ManyToManyField(
        Recipe, 'purchase_lists', through='RecipeInPurchaseList',
        through_fields=['purchase_list', 'recipe'], verbose_name='Рецепты',
        help_text='Рецепты, представленные в списке покупок')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'Список покупок #{self.id}'


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
