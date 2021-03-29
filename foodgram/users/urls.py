from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('registration/success', views.RegistrationSuccessView.as_view(),
         name='registration_success'),
    path('registration', views.RegistrationView.as_view(),
         name='registration'),
    path('favorites', views.FavoriteListView.as_view(),
         name='favorite_list'),
    path('subscriptions', views.SubscriptionListView.as_view(),
         name='subscription_list'),
    path('purchases/download', views.PurchaseListDownloadView.as_view(),
         name='purchase_list_download'),
    path('purchases', views.PurchaseListView.as_view(),
         name='purchase_list'),
]
