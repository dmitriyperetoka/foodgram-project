from django.urls import path

from . import views

urlpatterns = [
    path(
        '<str:username>/subscriptions', views.subscriptions,
        name='subscriptions'),
]
