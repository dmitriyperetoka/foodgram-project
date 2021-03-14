from django.contrib import admin

from .models import Favorite, Purchase, Subscription

admin.site.register(Favorite)
admin.site.register(Purchase)
admin.site.register(Subscription)
