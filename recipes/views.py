from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Recipe

User = get_user_model()


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
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Recipe.objects.filter(author=self.author)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class RecipeDetailView(DetailView):
    template_name = 'recipe_detail.html'
    model = Recipe
