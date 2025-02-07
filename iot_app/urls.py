from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('sobre', views.home, name='home'),
    path('contato', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Dashboard actions
    path('dashboard/cattle/<int:year>/', views.get_cattle_chart, name='chart-cattle'),
    path('dashboard/cattle/filter-options', views.get_filter_options, name='years-cattle-filter-options'),
    
    # Forms
    path('cadastro/gado', views.cattle_form_page, name='cattle-form'),
    path('cadastro/gado/rfid-sinal', views.get_rfid_sinal, name='rfid-sinal'),
    # path('register/gado/form', views.register_cattle_form, name='register_cattle_form'),
    
    # Listagens
    path('listagem/gado', views.cattle_list, name='cattle-list'),
    
    # API
    path('gerar-gado-aleatorio', views.criar_gado, name='criar-gado-aleatorio'),
    # path('api/cattle/feeding', views.get_cattle_feeding_data, name='get-cattle-feeding-data'),
]
