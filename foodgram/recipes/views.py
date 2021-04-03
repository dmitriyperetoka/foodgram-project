from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)


from .forms import RecipeForm
from .mixins import IsAuthorPermissionMixin
from .models import Recipe
from foodgram import settings

User = get_user_model()

RECIPE_LIST_QUERYSET = Recipe.objects.select_related(
    'author').prefetch_related(
    'favorite_lists__user', 'purchase_lists__user', 'tags')


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Create a single recipe."""

    success_url = reverse_lazy('recipes:recipe_list')
    form_class = RecipeForm
    model = Recipe

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeListView(ListView):
    """Display recipe list."""

    queryset = RECIPE_LIST_QUERYSET
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()

        tags = self.request.GET.getlist('tags')
        if tags:
            queryset.filter(tags__slug__in=tags)

        return queryset


class AuthorRecipeListView(ListView):
    """Display recipe list of a particular author."""

    queryset = RECIPE_LIST_QUERYSET
    paginate_by = settings.PAGINATE_BY
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = super().get_queryset().filter(author=self.author)

        tags = self.request.GET.getlist('tags')
        if tags:
            queryset.filter(tags__slug__in=tags)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class RecipeDetailView(DetailView):
    """Display a single recipe."""
    model = Recipe


class RecipeUpdateView(IsAuthorPermissionMixin, UpdateView):
    """Update a single recipe."""
    form_class = RecipeForm
    model = Recipe


class RecipeDeleteView(IsAuthorPermissionMixin, DeleteView):
    """Delete a single recipe."""
    success_url = reverse_lazy('recipes:recipe_list')
    model = Recipe
