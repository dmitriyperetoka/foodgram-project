from django.urls import path

from . import views

urlpatterns = [
    path('author/<str:username>', views.profile, name='profile'),
    path('id/<int:recipe_id>', views.recipe, name='recipe'),
    path('', views.main_page, name='main_page'),
]
