from django.contrib import admin

from .models import FavouriteRecipe, Subscription

admin.site.register(FavouriteRecipe)
admin.site.register(Subscription)
