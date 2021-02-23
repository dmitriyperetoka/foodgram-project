from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/favourites', views.favourites, name='favourites'),
    path(
        '<str:username>/subscriptions', views.subscriptions,
        name='subscriptions'),
]
