# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                 # frontend homepage
    path('signup/', views.signup, name='signup'),       # API endpoint with slash
    path('login/', views.login_view, name='login'),     # API endpoint with slash
    path('logout/', views.logout_view, name='logout'),  # API endpoint with slash
]