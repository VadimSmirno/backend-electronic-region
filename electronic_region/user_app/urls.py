from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logaut/', views.AuthenticationLogoutView.as_view(), name='logaut'),
    path('login/', views.AuthenticationLoginView.as_view(), name='login'),
]