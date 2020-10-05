from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signupuser(request):
    contex = {
        'form': UserCreationForm
    }
    return render(request, 'todo/signupuser.html', contex)