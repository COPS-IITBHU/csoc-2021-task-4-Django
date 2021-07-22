from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import *
# Create your views here.

def loginView(request):
    username = password = ''
    if request.POST:
        username= request.POST.get('username')
        password= request.POST.get('password')

        if(username=="" or password==""):
            messages.info(request, 'Please fill all fields')
            return redirect("/")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/store")
        
        else:
            messages.info(request, 'Inavlid Username/Password')
            return redirect("/")
                
    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logoutView(request):
    
    logout(request)
    return render(request,'login.html')

def registerView(request):
    if request.POST:
        reg_username= request.POST.get('regusername')
        reg_email = request.POST.get('email')
        reg_password = request.POST.get('regpassword')
        reg_name = request.POST.get('firstname')

        if(reg_username=="" or reg_password=="" or reg_email=="" or reg_name==""):
            messages.info(request, 'Please fill all fields')
            return redirect("/register")

        if User.objects.filter(username=reg_username).exists():
            messages.info(request, 'Username already exists')
            return redirect("/register")

        if User.objects.filter(email=reg_email).exists():
            messages.info(request, 'Email already exists')
            return redirect("/register")

        user = User.objects.create_user(reg_username, reg_email, reg_password)
        user.first_name = reg_name
        user.email = reg_email
        user.save()
        user = authenticate(username=reg_username, password=reg_password)
        if user is not None:
            login(request, user)
            return redirect("/store")

    return render(request,'register.html')