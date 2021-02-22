from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Store the records that certain users follow certain users."""

    subscriber = models.ForeignKey(
        User, models.CASCADE, 'favourite_authors', verbose_name='Подписчик',
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
