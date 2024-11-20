from django.shortcuts import render, redirect
from django.contrib.auth.forms import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

import json

# Create your views here.

def home(request):
    """Home page, apresentação do projeto"""
    
    return render(request, 'home.html')

def cadastro(request):
    """Página de cadastro"""
    
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return HttpResponse(
                status=404,
                headers={
                    'HX-Trigger': json.dumps({
                        "show-toast": {
                            "level": "error",
                            "title": "Algo deu errado!",
                            "message": "Senhas não coincidem, digite a mesma senha nos dois campos."
                        }
                    })
                }
            )

        else:
            user = User.objects.filter(username=username).first()
            
            if user :
                return HttpResponse(
                    status=404,
                    headers={
                        'HX-Trigger': json.dumps({
                            "show-toast": {
                                "level": "error",
                                "title": "Algo deu errado!",
                                "message": "Usuário já cadastrado."
                            }
                        })
                    }
                )
            else:
                user = User.objects.create_user(username, password=password)
                user.save()

                return HttpResponse(
                    status=201,
                    headers={
                        'HX-Trigger': json.dumps({
                            "show-toast": {
                                "level": "success",
                                "title": "Tudo certo! 👍",
                                "message": "Usuário cadastrado com sucesso."
                            }
                        })
                    }
                )

def login(request):
    """Página de login"""

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_django(request, user)
            
            HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "show-toast": {
                            "level": "success",
                            "title": "Tudo certo! 👍",
                            "message": "Login realizado com sucesso."
                        }
                    })
                }
            )
            
            return HTTPResponseHXRedirect('dashboard')
            
            return redirect('dashboard') # Redireciona para a página de dashboard


        else:
            return HttpResponse(
                status=404,
                headers={
                    'HX-Trigger': json.dumps({
                        "show-toast": {
                            "level": "error",
                            "title": "Algo deu errado!",
                            "message": "Usuário ou senha incorretos."
                        }
                    })
                }
            )
            
def logout(request):
    """Página de logout"""
    
    logout_django(request)
    
    return redirect('login')

def dashboard(request):
    """Página de dashboard"""
    
    if request.user.is_authenticated:        
        return render(request, 'dashboard.html')
    else:        
        return redirect('login')
    
class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200