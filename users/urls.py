from django.urls import include, path

from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(),
         name='registration'),
    path('favourites', views.FavouriteRecipesView.as_view(),
         name='favourites'),
    path('subscriptions', views.SubscriptionsView.as_view(),
         name='subscriptions'),
]
