from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView

from .forms import RegistrationForm
from recipes.models import Recipe

User = get_user_model()


class FavouriteRecipesView(ListView):
    template_name = 'favourite_recipes.html'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.objects.filter(favourite_lists__user=self.request.user)


class SubscriptionsView(ListView):
    template_name = 'subscriptions.html'

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user).prefetch_related(
            'recipes')


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = '/recipes/'
