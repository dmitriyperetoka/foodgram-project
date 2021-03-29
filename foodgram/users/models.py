from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Purchase(models.Model):
    """Store the records that certain recipes are in the purchase lists
    of certain users.
    """

    user = models.ForeignKey(
        User, models.CASCADE,
        'purchases', verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в список покупок')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE,
        'purchase_lists', verbose_name='Рецепт',
        help_text='Рецепт, представленный в списке покупок пользователя')

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списках покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} '
            f'в списке покупок у пользователя {self.user}')


class Favorite(models.Model):
    """Store the records that certain recipes are in the favorite lists
    of certain users.
    """

    user = models.ForeignKey(
        User, models.CASCADE, 'favorites', verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в список избранного')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, 'favorite_lists', verbose_name='Рецепт',
        help_text='Рецепт, который пользователь добавил в список избранного')

    class Meta:
        verbose_name = 'Рецепт в списке избранного'
        verbose_name_plural = 'Рецепты в списках избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')


class Subscription(models.Model):
    """Store the records that certain users follow certain users."""

    user = models.ForeignKey(
        User, models.CASCADE, 'subscriptions', verbose_name='Пользователь',
        help_text='Пользователь, который подписан на автора публикаций')
    author = models.ForeignKey(
        User, models.CASCADE, 'subscribers', verbose_name='Автор',
        help_text='Автор публикаций, на которого подписан пользователь')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_not_author'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан(а) на {self.author}'
