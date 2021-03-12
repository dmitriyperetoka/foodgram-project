from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import RecipeForm
from .models import Recipe

User = get_user_model()


class RecipeCreateView(LoginRequiredMixin, CreateView):
    success_url = '/recipes/'
    form_class = RecipeForm
    model = Recipe

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RecipeForm
    model = Recipe


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    success_url = '/recipes/'
    model = Recipe


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 3

    def get_queryset(self):
        tags = self.request.GET.getlist('tags')
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags)
        return super().get_queryset()


class AuthorRecipeListView(ListView):
    paginate_by = 3
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = Recipe.objects.filter(author=self.author)
        tags = self.request.GET.getlist('tags')

        if tags:
            return queryset.filter(tags__slug__in=tags)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class RecipeDetailView(DetailView):
    model = Recipe
