import os
import tempfile

from PIL import Image

from recipes.models import Recipe, Tag
from users.models import Favorite, Purchase, Subscription
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ModelsTestBase(TestCase):
    def check_field_list(self, instance, field_names, many_to_many=False):
        instance_fields = (
            instance._meta.many_to_many
            if many_to_many else instance._meta.fields)
        instance_field_names = [q.name for q in instance_fields]
        self.assertListEqual(instance_field_names, field_names)

    def check_field_classes(self, instance, field_classes):
        for field, _class in field_classes.items():
            with self.subTest():
                self.assertIsInstance(instance._meta.get_field(field), _class)

    def check_cascade(self, model, foreign_key, foreign_model, fm_instance):
        instance = model.objects.filter(**{foreign_key: fm_instance})
        with self.subTest():
            self.assertTrue(instance.exists())
        foreign_model.objects.get(id=fm_instance.id).delete()
        self.assertFalse(instance.exists())

    def check_related_names(self, instance, relations, one_to_one=False):
        for related_instance, related_name in relations:
            with self.subTest():
                if one_to_one:
                    query = related_instance.__getattribute__(related_name)
                    self.assertEqual(instance, query)
                else:
                    query = (
                        related_instance.__getattribute__(related_name).all())
                    self.assertIn(instance, query)

    def check_field_attrs(self, instance, field_attrs, remote=False):
        for field, attrs in field_attrs.items():
            for attr, value in attrs.items():
                with self.subTest():
                    instance_field = (
                        instance._meta.get_field(field).remote_field
                        if remote else instance._meta.get_field(field))
                    self.assertEqual(
                        instance_field.__getattribute__(attr), value)

    def check_model_attrs(self, instance, model_attrs):
        for attr, attr_value in model_attrs.items():
            with self.subTest():
                self.assertEqual(
                    instance._meta.__getattribute__(attr), attr_value)


class UrlsTestBase(TestCase):
    def check_exists(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def check_redirects(self, redirects, remote=False):
        for url, redirect_url in redirects.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertRedirects(
                    response, redirect_url,
                    fetch_redirect_response=False if remote else True)

    def check_redirect_chains(self, redirect_chains):
        for url, chain in redirect_chains.items():
            with self.subTest():
                response = self.client.get(url, follow=True)
                self.assertEqual(response.redirect_chain, chain)

    def check_unauthorized_forbidden(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def check_get_method_not_allowed(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 405)


class ViewsTestBase(TestCase):
    def check_template_used(self, reverse_names_templates):
        for reverse_name, template in reverse_names_templates:
            with self.subTest():
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_object_in_context(self, pages):
        for path, obj in pages:
            response = self.client.get(path)
            with self.subTest():
                self.assertEqual(response.context['object'], obj)

    def check_object_list_in_context(self, pages):
        for path, queryset, indexes in pages:
            response = self.client.get(path)
            with self.subTest():
                self.assertQuerysetEqual(
                    response.context['object_list'],
                    map(repr, queryset[indexes[0]:indexes[1]]))

    def check_extra_context_passed(self, pages):
        for path, extra_context in pages:
            response = self.client.get(path)
            for key, value in extra_context.items():
                with self.subTest():
                    self.assertEqual(response.context[key], value)


class RecipesViewsSetupBase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.client.force_login(self.user)
        self.another_user = User.objects.create(username='anotheruser')
        self.users = User.objects.all()

        tags = [
            Tag(title='Завтрак', slug='breakfast'),
            Tag(title='Обед', slug='lunch'),
            Tag(title='Ужин', slug='dinner'),
        ]
        Tag.objects.bulk_create(tags)
        self.tags = Tag.objects.all()

        self.fd, self.path = tempfile.mkstemp(suffix='.jpg')
        Image.new("RGB", (1, 1), "#000").save(self.path)

        self.recipe_kwargs = {
            'author': self.user, 'image': self.path,
            'title': 'Just some title', 'description': 'Just some description',
            'cooking_time_minutes': 60}
        self.recipe = Recipe.objects.create(**self.recipe_kwargs)

        recipes = []
        for q in range(29):
            self.recipe_kwargs.update(
                {'author': self.users[q % len(self.users)]})
            recipes.append(Recipe(**self.recipe_kwargs))
        Recipe.objects.bulk_create(recipes)

        for index, recipe in enumerate(Recipe.objects.all()):
            recipe.tags.set([self.tags[index % len(self.tags)]])

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)


class UsersViewsSetupBase(RecipesViewsSetupBase):
    def setUp(self):
        super().setUp()
        recipes = Recipe.objects.all()

        favorites = []
        for index, recipe in enumerate(recipes):
            if not index % 2:
                favorites.append(Favorite(user=self.user, recipe=recipe))
        Favorite.objects.bulk_create(favorites)

        purchases = []
        for index, recipe in enumerate(recipes):
            if not index % 3:
                favorites.append(Purchase(user=self.user, recipe=recipe))
        Favorite.objects.bulk_create(purchases)

        Subscription.objects.create(user=self.user, author=self.another_user)
