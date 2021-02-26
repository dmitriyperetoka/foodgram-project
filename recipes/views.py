from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Recipe

User = get_user_model()


def profile(request, **kwargs):
    return render(request, 'profile.html')


def recipe(request, **kwargs):
    return render(request, 'recipe_detail.html')


def new_recipe(request):
    return render(request, 'recipe_create.html')


class RecipeListView(ListView):
    template_name = 'recipe_list.html'
    model = Recipe
    paginate_by = 3


class AuthorRecipeListView(ListView):
    template_name = 'profile.html'
    paginate_by = 3

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return Recipe.objects.filter(author=author)


class RecipeDetailView(DetailView):
    template_name = 'recipe_detail.html'
    model = Recipe
