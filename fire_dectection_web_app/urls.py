from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('login/', views.LoginPage, name = "login"),
    path('logout/',views.LogoutPage,name='logout'),
]
