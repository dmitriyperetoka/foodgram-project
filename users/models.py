from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class FavoriteRecipe(models.Model):
    """Store the records that certain recipes are in the favourite lists
    of certain users.
    """

    user = models.ForeignKey(
        User, models.CASCADE, 'favorite_recipes', verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в список избранного')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, 'favorite_lists', verbose_name='Рецепт',
        help_text='Рецепт, который пользователь добавил в список избранного')

    class Meta:
        verbose_name = 'Рецепт в списке избранного'
        verbose_name_plural = 'Рецепты в списках избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} '
            f'в списке избранного у пользователя {self.user}')


class Subscription(models.Model):
    """Store the records that certain users follow certain users."""

    subscriber = models.ForeignKey(
        User, models.CASCADE, 'favorite_authors', verbose_name='Подписчик',
        help_text='Пользователь, который подписан на автора публикаций')
    author = models.ForeignKey(
        User, models.CASCADE, 'subscribers', verbose_name='Автор',
        help_text='Автор публикаций, на которого подписан пользователь')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscriber_author'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='subscriber_not_author'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан(а) на {self.author}'
