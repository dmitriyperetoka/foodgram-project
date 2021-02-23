from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:author_username>', views.profile, name='profile'),
    path('<str:author_username>/<int:recipe_id>', views.recipe, name='recipe'),
]
