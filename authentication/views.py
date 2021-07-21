from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:   
            return render(request,'login.html')
    return render(request,'login.html') 

def logoutView(request):
    logout(request)
    return redirect("/accounts/login")

def registerView(request):
    pass