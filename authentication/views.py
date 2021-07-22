from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# Create your views here.


@csrf_exempt
def loginView(request):
    return render(request, 'login.html')

@csrf_exempt
def loggingIn(request):
    if request.method=="POST":    
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username=username1, password=password1)
        if user is not None:
            login(request, user)
            return redirect("/books/")

            # A backend authenticated the credentials
        else:
            return render(request, 'login.html')
                # No backend authenticated the credentials
    

@csrf_exempt
def logoutView(request):
    pass


@csrf_exempt
def registerScreenView(request):
    return render(request, 'register.html')


@csrf_exempt
def registerView(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(
            username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        if user is not None:
            login(request, user)
            return redirect("/books/")
