from django.urls import path

from . import views

urlpatterns = [
    path(
        '<str:username>/<purchase_list_id>', views.purchase_list,
        name='purchase_list'),
]
