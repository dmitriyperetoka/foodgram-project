from django.urls import path

from . import views

urlpatterns = [
    path('new', views.NewPurchaseListView.as_view(),
         name='new_purchase_list'),
]
