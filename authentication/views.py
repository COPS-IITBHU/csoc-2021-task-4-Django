from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):
    
    template_name = 'authentication/login.html'

    if (request.method == 'POST') :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
        if (user is not None) :
            login(request, user)
            return redirect('/')
        return redirect('/accounts/login/')

    return render(request, template_name)

def logoutView(request):
    logout(request)
    return redirect('/')

def registerView(request):
    template_name = 'authentication/register.html'

    if (request.method == 'POST') :
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')

        if (User.objects.filter(email=email).exists()) :
            return redirect('/accounts/register/')

        if (User.objects.filter(username=username).exists()) :
            return redirect('/accounts/register/')

        user = User.objects.create_user(
            email=email, username=username, password=password, first_name=first_name)
        user.save()
        loggedIn = authenticate(username = username, password = password)
        login(request, loggedIn)
        return redirect('/')

    return render(request, template_name)