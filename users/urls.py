from django.urls import path

from . import views

urlpatterns = [
    path('favourites', views.FavouriteRecipesView.as_view(), name='favourites'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
]
