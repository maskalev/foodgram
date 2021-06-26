from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api import views

router_v1 = DefaultRouter()

router_v1.register('favorites', views.FavoritesView)
router_v1.register('purchases', views.PurchaseView)
router_v1.register('subscriptions', views.FollowView)

urlpatterns_api_v1 = [
    path('', include(router_v1.urls)),
    path('ingredients/',
         views.api_get_ingredients,
         name='get_ingredients'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_api_v1)),
]
