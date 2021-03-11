from django.contrib import admin

from .models import FavoriteRecipe, RecipeInPurchaseList, Subscription

admin.site.register(RecipeInPurchaseList)
admin.site.register(FavoriteRecipe)
admin.site.register(Subscription)
