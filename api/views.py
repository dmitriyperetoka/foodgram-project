from rest_framework import viewsets

from .serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=query)
