from django.urls import path

from apps.recipes import views

urlpatterns = [
    path('', views.RecipeList.as_view(), name='index'),
    path('<str:username>/recipes/', views.AuthorList.as_view(),
         name='authorlist'),
    path('add_recipe/',
         views.add_or_edit_recipe,
         name='add_recipe'),
    path('<str:username>/recipe/<slug:slug>/',
         views.RecipeDetail.as_view(),
         name='recipe'),
    path('<str:username>/recipe/<slug:slug>/edit/',
         views.add_or_edit_recipe,
         name='edit_recipe'),
    path('<str:username>/recipe/<slug:slug>/delete/',
         views.delete_recipe,
         name='delete_recipe'),
    path('<str:username>/recipe/<slug:slug>/confirm/',
         views.confirm_delete,
         name='confirm_delete'),
    path('favorites/', views.FavoritesList.as_view(), name='favorites'),
    path('subscriptions/', views.FollowList.as_view(),
         name='subscriptions'),
    path('purchases/', views.PurchaseList.as_view(),
         name='purchases'),
    path('subscriptions/download/',
         views.purchase_list_pdf,
         name='purchase_list_pdf'),
]
