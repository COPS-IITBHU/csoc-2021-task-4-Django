from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("store/")
        else:   
            return render(request,'login.html')
    return render(request,'login.html') 

def logoutView(request):
    logout(request)
    return redirect("/")

def registerView(request):
    return render(request,'register.html')

def registerform(request):
    if request.method=='POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('firstname')
        password=request.POST.get('password')
        user=User.objects.create_user(name,email,password)
        user.first_name=firstname
        user.save()
        return redirect('/')
    return render(request,'register.html')