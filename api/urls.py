from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    'ingredients', views.IngredientListViewSet, basename='ingredients')
router_v1.register(
    'favorites', views.FavoriteRecipeViewSet, basename='favorites')
router_v1.register(
    'purchases', views.RecipeInPurchaseListViewSet, basename='purchases')
router_v1.register(
    'subscriptions', views.SubscriptionsViewSet, basename='subscriptions')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
