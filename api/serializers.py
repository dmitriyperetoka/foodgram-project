from rest_framework import serializers

from recipes.models import Ingredient
from users.models import FavoriteRecipe
from purchases.models import RecipeInNewPurchaseList


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['recipe']


class RecipeInNewPurchaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInNewPurchaseList
        fields = ['recipe']
