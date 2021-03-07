from django.urls import include, path

from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(),
         name='registration'),
    path('favorites', views.FavoriteRecipesView.as_view(),
         name='favorites'),
    path('subscriptions', views.SubscriptionsView.as_view(),
         name='subscriptions'),
]
