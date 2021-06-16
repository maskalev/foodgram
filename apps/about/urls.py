from django.urls import path

from apps.about import views

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),
    path('foodgram/', views.AboutFoodgramView.as_view(), name='foodgram'),
]
