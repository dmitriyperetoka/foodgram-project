from django.db import models, utils
from django.contrib.auth import get_user_model

from ..models import Subscription
from recipes.tests.base_classes import ModelsTestBase

User = get_user_model()


class SubscriptionModelTest(ModelsTestBase):
    def setUp(self):
        self.subscriber = User.objects.create(username='some_user')
        self.author = User.objects.create(username='another_user')
        self.subscription = Subscription.objects.create(
            subscriber=self.subscriber, author=self.author)

    def test_field_list(self):
        field_names = ['id', 'subscriber', 'author']
        self.check_field_list(self.subscription, field_names)

    def test_field_classes(self):
        field_classes = {
            'subscriber': models.ForeignKey,
            'author': models.ForeignKey,
        }
        self.check_field_classes(self.subscription, field_classes)

    def test_cascade_subscriber(self):
        self.check_cascade(Subscription, 'subscriber', User, self.subscriber)

    def test_cascade_author(self):
        self.check_cascade(Subscription, 'author', User, self.author)

    def test_related_names(self):
        relations = [
            (self.subscriber, 'favourite_authors'),
            (self.author, 'subscribers'),
        ]
        self.check_related_names(self.subscription, relations)

    def test_field_attrs(self):
        field_attrs = {
            'subscriber': {
                'related_model': User,
                'verbose_name': 'Подписчик',
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
            'verbose_name': 'Подписка',
            'verbose_name_plural': 'Подписки',
        }
        self.check_model_attrs(self.subscription, model_attrs)

    def test_unique_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'UNIQUE constraint failed: '
                'users_subscription.subscriber_id, '
                'users_subscription.author_id'
        ):
            Subscription.objects.create(
                subscriber=self.subscriber, author=self.author)

    def test_not_self_constraint(self):
        with self.assertRaisesMessage(
                utils.IntegrityError,
                'CHECK constraint failed: subscriber_not_author'
        ):
            Subscription.objects.create(
                subscriber=self.subscriber, author=self.subscriber)

    def test_str(self):
        self.assertEqual(
            str(self.subscription),
            f'{self.subscription.subscriber} '
            f'подписан(а) на {self.subscription.author}')
