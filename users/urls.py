from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(),
         name='registration'),
    path('favorites', views.FavoriteRecipesView.as_view(),
         name='favorites'),
    path('subscriptions', views.SubscriptionsView.as_view(),
         name='subscriptions'),
    path('purchases', views.PurchaseListView.as_view(),
         name='purchases'),
]
