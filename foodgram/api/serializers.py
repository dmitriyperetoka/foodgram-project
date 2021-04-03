from rest_framework import serializers, validators

from .validators import NotEqualValidator
from recipes.models import Ingredient
from users.models import Favorite, Purchase, Subscription


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Purchase
        fields = ['user', 'recipe']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ['user', 'author']
        validators = [
            NotEqualValidator('user', 'author'),
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author']
            ),
        ]
