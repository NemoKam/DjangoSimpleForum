from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

from authapp.forms import UserRegisterForm, UserLoginForm
from profileapp.models import ProfileUser

from forum.settings import DOMAIN 


# Create your views here.
def user_register(request):
    if request.method == 'GET':
        register_form = UserRegisterForm()
        data = {
            'page_title': 'Register',
            'register_form': register_form
        }
        return render(request, 'authapp/register.html', data)
    else:
        register_form = UserRegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            try:
                EmailMessage('Подтверждение на сайте NemoKam',f'Чтобы подтвердить почту перейдите по ссылке: http://{DOMAIN}/auth/verify_email/{user.activation_key}', "kamstonks@mail.ru",  [user.email]).send()
            except Exception as e:
                return HttpResponse(f'Error while sending email: {e}')
            user.save()
            return HttpResponse('User registered')
        else:
            return HttpResponse(f'Invalid form: {register_form.errors}')
        
def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profileapp:profile')
        else:
            login_form = UserLoginForm()
            data = {
                'page_title': 'Login',
                'login_form': login_form
            }
            return render(request, 'authapp/login.html', data)
    else:
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            else:
                return HttpResponse('Incorrect Credentials')
            return redirect('profileapp:profile')
        elif login_form.cleaned_data['username'] and ProfileUser.objects.get(username=login_form.cleaned_data['username']):
            user = ProfileUser.objects.get(username=login_form.cleaned_data['username'])
            if not user.is_active:
                return HttpResponse('Activate your account. We send instruction to your email. Check it and follow instruction')
            else:
                return HttpResponse(f'Invalid form: {login_form.errors}')
        else:
            return HttpResponse(f'Invalid form: {login_form.errors}')
    
def user_logout(request):
    logout(request)
    return redirect('authapp:login')

def user_verify_email(request, activation_key):
    try:
        user = ProfileUser.objects.get(activation_key=activation_key)
        if user.is_active:
            return HttpResponse('Вы уже активировались')
        else:
            user.is_active = True
            user.save()
    except ObjectDoesNotExist:
        return HttpResponse('Неверный ключ активации')
    return redirect('profileapp:profile_create')
