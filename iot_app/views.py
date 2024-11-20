from django.shortcuts import render
from django.contrib.auth.forms import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
                    status=404,
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
    
    return render(request, 'login.html')

