from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SubscriptionForm
from .models import Favorite, Purchase, Subscription

UserAdmin.list_filter += ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm


admin.site.register(Favorite)
admin.site.register(Purchase)
