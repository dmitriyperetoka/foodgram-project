from rest_framework import serializers

from recipes.models import Ingredient
from users.models import FavoriteRecipe, RecipeInPurchaseList, Subscription


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['recipe']


class RecipeInPurchaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInPurchaseList
        fields = ['recipe']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['author']
