from django.urls import path

from . import views

urlpatterns = [
    path('favourites/<str:username>', views.favourites, name='favourites'),
    path(
        'subscriptions/<str:username>', views.subscriptions,
        name='subscriptions'),
]
