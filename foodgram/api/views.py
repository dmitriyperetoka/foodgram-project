from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from .permissions import IsOwnerPermission
from .serializers import (
    FavoriteSerializer, IngredientSerializer,
    PurchaseSerializer, SubscriptionSerializer,
)
from recipes.models import Ingredient
from users.models import Favorite, Purchase, Subscription

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Return filtered ingredients list."""

    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=query)


class CustomCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Implement common methods for creating and destroying views."""
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]


class FavoriteViewSet(CustomCreateDestroyViewSet):
    """Create and destroy records of adding recipe to favorite list."""

    serializer_class = FavoriteSerializer

    def get_object(self):
        return get_object_or_404(
            Favorite, user=self.request.user, recipe=self.kwargs.get('pk'))


class PurchaseViewSet(CustomCreateDestroyViewSet):
    """Create and destroy records of adding recipe to purchase list."""

    serializer_class = PurchaseSerializer

    def get_object(self):
        return get_object_or_404(
            Purchase, user=self.request.user, recipe=self.kwargs.get('pk'))


class SubscriptionViewSet(CustomCreateDestroyViewSet):
    """Create and destroy records of subscription to an author."""

    serializer_class = SubscriptionSerializer

    def get_object(self):
        return get_object_or_404(
            Subscription, user=self.request.user, author=self.kwargs.get('pk'))
