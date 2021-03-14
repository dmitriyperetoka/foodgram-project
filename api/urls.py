from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    'ingredients', views.IngredientViewSet, basename='ingredients')
router_v1.register(
    'favorites', views.FavoriteViewSet, basename='favorites')
router_v1.register(
    'purchases', views.PurchaseViewSet, basename='purchases')
router_v1.register(
    'subscriptions', views.SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
