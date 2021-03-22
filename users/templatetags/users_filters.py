from django import template
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()

register = template.Library()


@register.filter
def request_user_favorites(request, recipe):
    return recipe in Recipe.objects.filter(favorite_lists__user=request.user)


@register.filter
def request_user_purchases(request, recipe):
    return recipe in Recipe.objects.filter(
        purchase_lists__user=request.user)


@register.filter
def request_user_subscriptions(request, author):
    return author in User.objects.filter(subscribers__user=request.user)
