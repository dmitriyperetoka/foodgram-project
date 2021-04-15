import os

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ..models import Subscription
from foodgram.settings import BASE_DIR

User = get_user_model()


@override_settings(STATIC_ROOT=os.path.join(BASE_DIR, 'static'))
class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser')
        self.client.force_login(self.superuser)
        self.another_user = User.objects.create(username='anotheruser')

    def test_subscription_form(self):
        initial_subscription_count = Subscription.objects.count()
        url = '/admin/users/subscription/add/'

        response = self.client.post(url, follow=True)

        with self.subTest():
            self.assertListEqual(
                response.context['errors'],
                [['Обязательное поле.'], ['Обязательное поле.']])

        response = self.client.post(
            url, data={'user': self.superuser.id, 'author': self.superuser.id},
            follow=True)

        with self.subTest():
            self.assertListEqual(
                response.context['errors'],
                [['Нельзя подписываться на себя.']])

        with self.subTest():
            self.assertEqual(
                Subscription.objects.count(), initial_subscription_count)

        self.client.post(
            url,
            data={'user': self.superuser.id, 'author': self.another_user.id},
            follow=True)

        with self.subTest():
            self.assertEqual(
                Subscription.objects.count(), initial_subscription_count + 1)

        response = self.client.post(
            url,
            data={'user': self.superuser.id, 'author': self.another_user.id},
            follow=True)

        with self.subTest():
            self.assertListEqual(
                response.context['errors'],
                [['Подписка с такими значениями полей Пользователь и Автор '
                  'уже существует.']])

        with self.subTest():
            self.assertEqual(
                Subscription.objects.count(), initial_subscription_count + 1)
