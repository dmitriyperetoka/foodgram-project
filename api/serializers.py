from rest_framework import serializers

from recipes.models import Ingredient
from users.models import FavouriteRecipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavouriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteRecipe
        fields = ['recipe']
