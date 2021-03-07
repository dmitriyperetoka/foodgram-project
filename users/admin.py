from django.contrib import admin

from .models import FavoriteRecipe, Subscription

admin.site.register(FavoriteRecipe)
admin.site.register(Subscription)
