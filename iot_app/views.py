from datetime import datetime, timezone
import random
import serial
import time
from django.shortcuts import render, redirect
from django.contrib.auth.forms import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import ExtractMonth, ExtractYear
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import F, Sum, Count
from utils.charts import months, colorPrimary, get_year_dict
from django.http import JsonResponse
from iot_app.models import Cattle, Fertility, Vaccination, RfidMetrics
from faker import Faker

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
            
            return HTTPResponseHXRedirect('dashboard')

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
        
        total_registros = RfidMetrics.objects.count()
        total_gado = Cattle.objects.count()
        
        return render(request, 'dashboard.html', {
            'total_registros': total_registros,
            'total_gado': total_gado
        })
    else:        
        return redirect('login')

def cattle_form_page(request):
    """Página de formulário de cadastro de gado"""
    
    rfid_value = request.GET.get('rfid_value')
    
    if request.user.is_authenticated == False:
        return redirect('login')
    
    if request.method == 'GET':
        return render(request, 'forms/form-cattle.html', {
            'rfid_value': rfid_value or ''
        })
    if request.method == 'POST': 
        nameCattle = request.POST.get('nameCattle')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        description = request.POST.get('description')
        birth_weight = request.POST.get('birth_weight')
        weaning_weight = request.POST.get('weaning_weight')
        slaughter_weight = request.POST.get('slaughter_weight')
        father = request.POST.get('father') or None
        mother = request.POST.get('mother') or None
        created_at = datetime.now()
        updated_at = datetime.now()
                
        # Criação do objeto Cattle no banco de dados
        cattle = Cattle.objects.create(
            RFID=rfid_value,
            nameCattle=nameCattle,
            gender=gender,
            birth_date=birth_date,
            description=description,
            birth_weight=birth_weight,
            weaning_weight=weaning_weight,
            slaughter_weight=slaughter_weight,
            father=father,
            mother=mother,
            created_at=created_at,
            updated_at=updated_at
        )

        cattle.save()

        return HttpResponse(
            status=201,
            headers={
                'HX-Trigger': json.dumps({
                    "show-toast": {
                        "level": "success",
                        "title": "Cadastro realizado com sucesso!",
                        "message": "O gado" + cattle.nameCattle + " foi cadastrado com sucesso."
                    }
                })
            }
        )

def register_cattle_form(request):
    """Página de cadastro de gado"""

    print(request.POST, "Testeeeeeeee")
    
    gender = request.POST.get('gender')
    birth_date = request.POST.get('birth_date')
    description = request.POST.get('description')
    birth_weight = request.POST.get('birth_weight')
    weaning_weight = request.POST.get('weaning_weight')
    slaughter_weight = request.POST.get('slaughter_weight')
    father = request.POST.get('father')
    mother = request.POST.get('mother')
    
    # Criação do objeto Cattle no banco de dados
    cattle = Cattle.objects.create(
        RFID=None,
        gender=gender,
        birth_date=birth_date,
        description=description,
        birth_weight=birth_weight,
        weaning_weight=weaning_weight,
        slaughter_weight=slaughter_weight,
        father=father,
        mother=mother
    )

    cattle.save()
    
    return JsonResponse({
        "rfid_value": cattle.RFID
    })

@csrf_protect
def get_rfid_sinal(request):
    """Mecanismo para captar sinal do arduindo e do RFID"""
    
    if request.method == 'POST':
        # Adjust the COM port and baud rate to match your Arduino settings
        arduino = serial.Serial('COM5', 9600, timeout=1)
        
        time.sleep(2)  # Espera o Arduino inicializar

        while True:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                print("Resposta do Arduino:", data)
                break
            
        arduino.close()
        
        return JsonResponse({
            "rfid_value":  data.replace("UID da tag : ", "")
        })

    if request.user.is_authenticated:        
        return render(request, 'forms/form-cattle.html')
    else:        
        return redirect('login')

def get_filter_options(request):
    options = []

    grouped_cattle = Cattle.objects.annotate(year=ExtractYear("created_at")).values("year").order_by("-year").distinct()
        
    if(grouped_cattle.count() == 0):
            options = [datetime.now().year]
    else:
        options = [cattle["year"] for cattle in grouped_cattle]

    print(options)
    
    return JsonResponse({
        "options": options,
    })

def get_cattle_chart(request, year):
        
    catties = Cattle.objects.values()
        
    if(catties.count() == 0):
        return HttpResponse('Não há cattle cadastrados para o ano selecionado')

    created_count_by_month = catties.filter(created_at__year=year).annotate(month=ExtractMonth("created_at")).values("month").annotate(created_count=Count('id'))
        
    print('created_count_by_month:', created_count_by_month)

    sales_dict = get_year_dict()

    for group in created_count_by_month:
        sales_dict[months[group["month"]-1]] = round(group["created_count"], 2)
        
    return JsonResponse({
        "title": f"Gado registrado no ano de {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Quantidade: ",
                "fill": True,
                "borderColor": colorPrimary,
                "tension": 0.2,
                "data": list(sales_dict.values()),
            }]
        },
    }) 

# @csrf_exempt
# def get_cattle_feeding_data(request):
#     """Método para obter dados de alimentação de gado"""
           
#     # Pegar o ano da request
#     UID_data = request.POST["UID"]
#     first_read = request.POST["first_read"]
#     last_read = request.POST["last_read"]
#     duration_seconds = request.POST["duration_seconds"]
    
#     rfid_metrics = RfidMetrics.objects.create(cattle_id = UID_data, activation_time = first_read, deactivation_time = last_read, duration_seconds = duration_seconds)
#     rfid_metrics.save()
    
#     return HttpResponse(
#                     status=204,
#                     headers={
#                         'HX-Trigger': json.dumps({
#                             "show-toast": {
#                                 "level": "success",
#                                 "title": "Tudo certo! 👍",
#                                 "message": "Registro de alimentação realizado com sucesso."
#                             }
#                         })
#                     }
#                 )

fake = Faker()

def gerar_rfid():
    return random.choice(['2e c7 91 ab', '53 e6 d8 9a', 'c1 47 0c 19'])

def gerar_gender():
    return random.choice(['Male', 'Female'])

def gerar_birth_weight():
    return random.uniform(5.0, 20.0)

def gerar_weaning_weight():
    return random.uniform(15.0, 40.0)

def gerar_slaughter_weight():
    return random.uniform(30.0, 100.0)

def gerar_birth_date():
    return fake.date_of_birth(minimum_age=0, maximum_age=5)

def gerar_description():
    return fake.sentence()

def gerar_created_at():
    created_at_naive = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    
    return created_at_naive

# Função de view que cria dados aleatórios
def criar_gado(request):
    # Gera dados aleatórios e cria 5 objetos Cattle
    for _ in range(5):
        RFID = gerar_rfid()
        gender = gerar_gender()
        birth_date = gerar_birth_date()
        description = gerar_description()
        birth_weight = gerar_birth_weight()
        weaning_weight = gerar_weaning_weight()
        slaughter_weight = gerar_slaughter_weight()
        created_at = gerar_created_at()
        father = None  # Você pode associar o pai, se necessário
        mother = None  # Você pode associar a mãe, se necessário
        
        print(created_at)

        # Criação do objeto Cattle no banco de dados
        Cattle.objects.create(
            RFID=RFID,
            gender=gender,
            birth_date=birth_date,
            description=description,
            birth_weight=birth_weight,
            weaning_weight=weaning_weight,
            slaughter_weight=slaughter_weight,
            created_at=created_at,
            father=father,
            mother=mother
        )

    # Retorna uma resposta HTTP indicando que os dados foram criados
    return HttpResponse(
                headers={
                    'HX-Trigger': json.dumps({
                        "show-toast": {
                            "level": "success",
                            "title": "Tudo certo! 👍",
                            "message": "Dados aleatórios criados com sucesso."
                        }
                    })
                }
            )

class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200