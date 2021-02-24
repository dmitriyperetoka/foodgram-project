from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('<str:username>', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>', views.recipe, name='recipe'),
]
