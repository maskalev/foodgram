from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api import views

router_v1 = DefaultRouter()

router_v1.register('favorites', views.FavoritesView)
router_v1.register('purchases', views.PurchaseView)
router_v1.register('subscriptions', views.FollowView)
router_v1.register('ingredients', views.IngredientsView)


urlpatterns_api_v1 = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_api_v1)),
]
