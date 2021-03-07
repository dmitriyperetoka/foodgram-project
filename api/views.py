from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from .serializers import FavouriteRecipeSerializer, IngredientSerializer
from recipes.models import Recipe, Ingredient
from users.models import FavouriteRecipe


class IngredientListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=query)


class FavouriteRecipeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FavouriteRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('recipe'))
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        return get_object_or_404(
            FavouriteRecipe, user=self.request.user, recipe=self.kwargs.get('pk'))
