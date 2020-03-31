from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path("", views.ProfileView.as_view(), name='profile'),

    # path('reg/', views.register, name='reg'),
    path('registr/', views.RegistrationView.as_view(), name='regtest'),
    # path('reg/', views.RegisterView.as_view(), name='reg'),
    path("login/", authViews.LoginView.as_view(), name='login'),
    path("logout/", views.LogOutView.as_view(), name='logout'),


]
