from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect('/')
        return redirect('/accounts/login')

    return render(request, 'store/login.html')


def logoutView(request):
    logout(request)
    return redirect('/')


def registerView(request):

    if (request.method == 'POST'):

        username = request.POST.get('username')
        password = request.POST.get('password')
  
        if (User.objects.filter(username=username).exists()):
            return redirect('/accounts/register')

        user = User.objects.create_user(
            username=username, password=password)
        user.save()
        loggedIn = authenticate(username=username, password=password)
        login(request, loggedIn)
        return redirect('/')

    return render(request, 'store/register.html')
