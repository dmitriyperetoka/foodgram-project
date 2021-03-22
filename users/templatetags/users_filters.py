from django import template
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()

register = template.Library()


@register.filter
def favorites(user, recipe):
    return recipe in Recipe.objects.filter(favorite_lists__user=user)


@register.filter
def purchases(user, recipe):
    return recipe in Recipe.objects.filter(
        purchase_lists__user=user)


@register.filter
def subscriptions(user, author):
    return author in User.objects.filter(subscribers__user=user)
