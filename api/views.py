from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from .serializers import (
    FavoriteRecipeSerializer, IngredientSerializer,
    RecipeInPurchaseListSerializer, SubscriptionSerializer,
)
from recipes.models import Recipe, Ingredient
from users.models import FavoriteRecipe, RecipeInPurchaseList, Subscription

User = get_user_model()


class IngredientListViewSet(viewsets.ReadOnlyModelViewSet):
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


class FavoriteRecipeViewSet(CustomCreateDestroyViewSet):
    serializer_class = FavoriteRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    def get_object(self):
        return get_object_or_404(
            FavoriteRecipe, user=self.request.user,
            recipe=self.kwargs.get('pk'))


class RecipeInPurchaseListViewSet(CustomCreateDestroyViewSet):
    serializer_class = RecipeInPurchaseListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    def get_object(self):
        return get_object_or_404(
            RecipeInPurchaseList, user=self.request.user,
            recipe=self.kwargs.get('pk'))


class SubscriptionsViewSet(CustomCreateDestroyViewSet):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        serializer.save(subscriber=self.request.user, author=author)

    def get_object(self):
        return get_object_or_404(
            Subscription, subscriber=self.request.user,
            author=self.kwargs.get('pk'))
