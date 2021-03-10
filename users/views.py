from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator

from .forms import RegistrationForm
from recipes.models import Recipe

User = get_user_model()


@method_decorator(login_required, 'dispatch')
class FavoriteRecipesView(ListView):
    template_name = 'users/favorites.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.filter(
            favorite_lists__user=self.request.user)
        tags = self.request.GET.getlist('tags')

        if tags:
            return queryset.filter(tags__slug__in=tags)

        return queryset


@method_decorator(login_required, 'dispatch')
class SubscriptionsView(ListView):
    template_name = 'users/subscriptions.html'

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user).prefetch_related(
            'recipes')


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = '/recipes/'
