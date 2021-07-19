from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):
    context={
        "visibility":"none",
    }
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html',context)
    return render(request, 'login.html',context)

def logoutView(request):
    logout(request)
    context={
        'visibility':"",
    }
    return render(request, 'login.html',context)

def registerView(request):
    context={
        'visibility':"none",
    }
    if request.method=="POST":
        name = request.POST.get('name')
        username= request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            context['visibility']=""
            return render(request, 'register.html',context)
        user = User.objects.create_user(username,email,password)
        user.first_name=name
        if user is not None:
            user.save()
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'register.html',context)
    return render(request, 'register.html',context)