from django.shortcuts import render
from django.contrib.auth.forms import User
from django.http import HttpResponse
# Create your views here.

def home(request):
    """Home page, apresentação do projeto"""
    
    return render(request, 'home.html')

def register(request):
    """Página de cadastro"""
    
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return HttpResponse('Senhas nao sao iguais')
        
        else:
            user = User.objects.filter(username=username).first()
            
            if user :
                return HttpResponse('Usuário já cadastrado')
            else:
                user = User.objects.create_user(username, password=password)
                user.save()

                return HttpResponse('Usuário cadastrado com sucesso')

def login(request):
    """Página de login"""
    
    return render(request, 'login.html')

