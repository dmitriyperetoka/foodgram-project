import re

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View

from .forms import RegistrationForm
from .services import PurchaseListFileContentMaker
from recipes.models import Recipe

User = get_user_model()


class SubscriptionListView(LoginRequiredMixin, ListView):
    """Display list of authors that the user is subscribed to."""

    def get_queryset(self):
        return self.request.user.subscriptions.select_related(
            'author').prefetch_related('author__recipes')


class PurchaseListView(LoginRequiredMixin, ListView):
    """Display recipes that are in the purchase list of the user."""

    def get_queryset(self):
        return self.request.user.purchases.select_related('recipe')


class PurchaseListDownloadView(LoginRequiredMixin, View):
    """Download a file with a purchase list."""

    @staticmethod
    def get(request):
        content = PurchaseListFileContentMaker().make(request.user)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=purchases.txt'
        return response


class FavoriteListView(LoginRequiredMixin, ListView):
    """Display recipes that are in the favorite list of the user."""

    template_name = 'users/favorite_list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.filter(
            favorite_lists__user=self.request.user).select_related('author')
        tags = self.request.GET.getlist('tags')

        if tags:
            return queryset.filter(tags__slug__in=tags)

        return queryset


class RegistrationView(CreateView):
    """Register new user."""

    template_name = 'registration/registration.html'
    success_url = reverse_lazy('users:registration_success')
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=self.request.POST['username'],
            password=self.request.POST['password1'])
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class RegistrationSuccessView(TemplateView):
    """Display registration success page."""

    template_name = 'registration/registration_success.html'

    def get(self, request, *args, **kwargs):
        host = request.META.get('HTTP_HOST')
        path = reverse('users:registration')
        regexp = fr'^https?://{host}{path}$'
        referer = request.META.get('HTTP_REFERER')

        if referer is not None and re.match(regexp, referer):
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('main_page'))
