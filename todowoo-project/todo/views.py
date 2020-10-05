from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        contex = {
            'form': UserCreationForm,
        }
        return render(request, 'todo/signupuser.html', contex)
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Create a new user
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
        else:
            # Passwords dodn't match
            contex = {
                'form': UserCreationForm,
                'error': 'Podane hasła są różne!',
            }
            return render(request, 'todo/signupuser.html', contex)
