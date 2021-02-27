from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import ListView

from recipes.models import Recipe

User = get_user_model()


def subscriptions(request, **kwargs):
    return render(request, 'subscriptions.html')


class FavouriteRecipesView(ListView):
    template_name = 'favourite_recipes.html'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.objects.filter(favourite_lists__user=self.request.user)
