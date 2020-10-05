from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout

# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        contex = {
            'form': UserCreationForm,
        }
        return render(request, 'todo/signupuser.html', contex)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Create a new user
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                # User login
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                contex = {
                    'form': UserCreationForm,
                    'error': 'Podana nazwa użytkownika już istnieje!',
                }
                return render(request, 'todo/signupuser.html', contex)
        else:
            # Passwords dodn't match
            contex = {
                'form': UserCreationForm,
                'error': 'Podane hasła są różne!',
            }
            return render(request, 'todo/signupuser.html', contex)

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todo/home.html')
