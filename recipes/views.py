from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.utils.decorators import method_decorator

from .forms import RecipeCreateForm
from .models import Recipe

User = get_user_model()


@method_decorator(login_required, 'dispatch')
class RecipeCreateView(CreateView):
    template_name = 'recipe_create.html'
    form_class = RecipeCreateForm
    success_url = '/recipes/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeListView(ListView):
    template_name = 'recipe_list.html'
    model = Recipe
    paginate_by = 3

    def get_queryset(self):
        tags = self.request.GET.getlist('tags')
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags)
        return super().get_queryset()


class AuthorRecipeListView(ListView):
    template_name = 'profile.html'
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
    template_name = 'recipe_detail.html'
    model = Recipe
