from django.urls import path

from apps.users import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]