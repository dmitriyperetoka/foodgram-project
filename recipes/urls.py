from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:author_username>', views.author_recipes, name='author_recipes'),
    path('<str:author_username>/<int:recipe_id>', views.recipe, name='recipe'),
]
