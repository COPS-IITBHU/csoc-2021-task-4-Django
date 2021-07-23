from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from library.forms import SignUpForm
# Create your views here.


def loginView(request):
    if request.method == 'GET':
        return render(request,'authentication/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'authentication/login.html',{'form':AuthenticationForm(),'error':'Username and Password did not match.'})
        else:
            login(request,user)
            return redirect('index')

def logoutView(request):
    return redirect('index')

def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})