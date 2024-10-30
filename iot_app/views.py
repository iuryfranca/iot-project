from django.shortcuts import render

# Create your views here.

def home(request):
    """Home page, apresentação do projeto"""
    
    return render(request, 'home.html')

def login(request):
    """Página de login"""
    
    return render(request, 'login.html')
