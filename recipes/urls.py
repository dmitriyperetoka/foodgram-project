from django.urls import path

from . import views

urlpatterns = [
    path('author/<str:username>', views.AuthorRecipeListView.as_view(),
         name='profile'),
    path('id/<int:pk>/edit', views.RecipeUpdateView.as_view(),
         name='recipe_update'),
    path('id/<int:pk>/delete', views.RecipeDeleteView.as_view(),
         name='recipe_delete'),
    path('id/<int:pk>', views.RecipeDetailView.as_view(),
         name='recipe_detail'),
    path('new', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('', views.RecipeListView.as_view(), name='recipe_list'),
]
