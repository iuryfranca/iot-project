from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.home, name='home'),
    path('contato', views.home, name='home'),
    path('login', views.login, name='login'),
]
