import os
import tempfile

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from PIL import Image

from recipes.models import Ingredient, Recipe
from users.models import Favorite, Purchase, Subscription

User = get_user_model()


class APIDisplayViewsTest(TestCase):
    def test_ingredients(self):
        preset = [
            {'title': 'Just an ingredient', 'dimension': 'g'},
            {'title': 'Just another ingredient', 'dimension': 'l'},
            {'title': 'Whatever ingredient', 'dimension': 'pc'},
        ]
        ingredients = []

        for item in preset:
            ingredients.append(
                Ingredient(title=item['title'], dimension=item['dimension']))

        Ingredient.objects.bulk_create(ingredients)
        response = self.client.get(reverse('api:ingredients-list'))

        with self.subTest():
            self.assertEqual(response.json(), preset)

        queries = {
            '': preset,
            'word': [],
            'ju': preset[:2],
            'ver': preset[2:],
            'ingredient': preset,
        }
        for query, fetch in queries.items():
            with self.subTest():
                response = self.client.get(
                    reverse('api:ingredients-list') + f'?query={query}')
                self.assertEqual(response.json(), fetch)


class APICreateDestroyViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='someuser')
        self.client.force_login(self.user)

        self.another_user = User.objects.create(username='anotheruser')
        self.fd, self.path = tempfile.mkstemp(suffix='.jpg')
        Image.new("RGB", (1, 1), "#000").save(self.path)
        self.recipe = Recipe.objects.create(
            author=self.another_user, image=self.path, cooking_time_minutes=60)

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    def check_exists(self, model, obj, field):
        return model.objects.filter(**{'user': self.user, field: obj}).exists()

    def check_relation_create_destroy(self, model, obj, field, basename):
        args_ = [model, obj, field]

        with self.subTest():
            self.assertFalse(self.check_exists(*args_))

        self.client.post(
            reverse(f'api:{basename}-list'), data={field: obj.id})
        with self.subTest():
            self.assertTrue(self.check_exists(*args_))

        response = self.client.post(
            reverse(f'api:{basename}-list'), data={field: obj.id})
        with self.subTest():
            self.assertEqual(response.status_code, 400)

        self.client.delete(
            reverse(f'api:{basename}-detail', args=[obj.id]))
        with self.subTest():
            self.assertFalse(self.check_exists(*args_))

        response = self.client.delete(
            reverse(f'api:{basename}-detail', args=[obj.id]))
        with self.subTest():
            self.assertEqual(response.status_code, 404)

    def test_purchases(self):
        self.check_relation_create_destroy(
            Purchase, self.recipe, 'recipe', 'purchases')

    def test_favorites(self):
        self.check_relation_create_destroy(
            Favorite, self.recipe, 'recipe', 'favorites')

    def test_subscriptions(self):
        self.check_relation_create_destroy(
            Subscription, self.another_user, 'author', 'subscriptions')
