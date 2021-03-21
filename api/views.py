from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from .serializers import (
    FavoriteSerializer, IngredientSerializer,
    PurchaseSerializer, SubscriptionSerializer,
)
from recipes.models import Recipe, Ingredient
from users.models import Favorite, Purchase, Subscription

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=query)


class CustomCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.request.data.get('recipe'))


class FavoriteViewSet(CustomCreateDestroyViewSet):
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    def get_object(self):
        return get_object_or_404(
            Favorite, user=self.request.user,
            recipe=self.kwargs.get('pk'))


class PurchaseViewSet(CustomCreateDestroyViewSet):
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    def get_object(self):
        return get_object_or_404(
            Purchase, user=self.request.user,
            recipe=self.kwargs.get('pk'))


class SubscriptionViewSet(CustomCreateDestroyViewSet):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        serializer.save(user=self.request.user, author=author)

    def get_object(self):
        return get_object_or_404(
            Subscription, user=self.request.user,
            author=self.kwargs.get('pk'))
