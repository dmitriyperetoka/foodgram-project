from django.urls import path

from . import views

urlpatterns = [
    path('new', views.purchase_list, name='new_purchase_list'),
    path('<purchase_list_id>', views.purchase_list, name='purchase_list'),
]
