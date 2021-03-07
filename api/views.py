from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from .serializers import (
    FavoriteRecipeSerializer, IngredientSerializer,
    RecipeInNewPurchaseListSerializer,
)
from purchases.models import NewPurchaseList, RecipeInNewPurchaseList
from recipes.models import Recipe, Ingredient
from users.models import FavoriteRecipe


class IngredientListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=query)


class FavoriteRecipeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('recipe'))
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        return get_object_or_404(
            FavoriteRecipe, user=self.request.user, recipe=self.kwargs.get('pk'))


class RecipeInNewPurchaseListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RecipeInNewPurchaseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_new_purchase_list(self):
        return NewPurchaseList.objects.get_or_create(
            author=self.request.user)[0]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('recipe'))
        serializer.save(
            new_purchase_list=self.get_new_purchase_list(), recipe=recipe)

    def get_object(self):
        return get_object_or_404(
            RecipeInNewPurchaseList,
            new_purchase_list=self.get_new_purchase_list(),
            recipe=self.kwargs.get('pk'))
