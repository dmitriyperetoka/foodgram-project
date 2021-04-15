from django import template
from django.contrib.auth import get_user_model

from ..models import Favorite, Purchase, Subscription

User = get_user_model()

register = template.Library()


@register.filter
def favorites(user, recipe):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def purchases(user, recipe):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def subscriptions(user, author):
    return Subscription.objects.filter(user=user, author=author).exists()
