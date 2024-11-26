from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.home, name='home'),
    path('contato', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/cattle/<int:year>/', views.get_cattle_chart, name='chart-cattle'),
    path('dashboard/cattle/filter-options', views.get_filter_options, name='years-cattle-filter-options'),
]
