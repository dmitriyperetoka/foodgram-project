from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(),
         name='registration'),
    path('favorites', views.FavoriteListView.as_view(),
         name='favorites'),
    path('subscriptions', views.SubscriptionListView.as_view(),
         name='subscriptions'),
    path('purchases/download', views.PurchaseListDownloadView.as_view(),
         name='download_purchases'),
    path('purchases', views.PurchaseListView.as_view(),
         name='purchases'),
]
