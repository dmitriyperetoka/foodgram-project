from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import CreateView, ListView, View

from .forms import RegistrationForm
from .services import make_file_content
from recipes.models import Recipe

User = get_user_model()


class PurchaseListView(LoginRequiredMixin, ListView):
    template_name = 'users/purchases.html'

    def get_queryset(self):
        return self.request.user.purchases.select_related('recipe')


class PurchaseListDownloadView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        content = make_file_content(request.user)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=purchases.txt'
        return response


class FavoriteRecipesView(LoginRequiredMixin, ListView):
    template_name = 'users/favorites.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.filter(
            favorite_lists__user=self.request.user)
        tags = self.request.GET.getlist('tags')

        if tags:
            return queryset.filter(tags__slug__in=tags)

        return queryset


class SubscriptionsView(LoginRequiredMixin, ListView):
    template_name = 'users/subscriptions.html'

    def get_queryset(self):
        return User.objects.filter(
            subscribers__user=self.request.user
        ).prefetch_related('recipes')


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = '/recipes/'
