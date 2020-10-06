from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

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
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    contex = {
        'todos': todos,
    }
    return render(request, 'todo/currenttodos.html', contex)

def loginuser(request):
    if request.method == 'GET':
        contex = {
            'form': AuthenticationForm,
        }
        return render(request, 'todo/loginuser.html', contex)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            contex = {
                'form': AuthenticationForm,
                'error': 'Podana nazwa użytkownika lub hasło jest nieprawidłowe!',
            }
            return render(request, 'todo/loginuser.html', contex)
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todo/home.html')

def createtodos(request):
    if request.method == 'GET':
        context = {
            'form': TodoForm,
        }
        return render(request, 'todo/createtodo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            context = {
                'form': TodoForm,
                'error': 'Nieodpowiednie dane',
            }
            return render(request, 'todo/createtodo.html', context)

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'todo': todo,
            'form': form,
        }
        return render(request, 'todo/viewtodo.html', context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            context = {
                'form': todo,
                'form': form,
                'error': 'Nieodpowiednie dane',
            }
            return render(request, 'todo/viewtodo.html', context)