import json

from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User, auth
# Create your views here.

dataDictionary = {'cas': 0}
dataJSON = json.dumps(dataDictionary)
dataDictionary1 = {'cas': 1}
dataJSON1 = json.dumps(dataDictionary1)
dataDictionary2 = {'cas': 2}
dataJSON2 = json.dumps(dataDictionary2)


def loginView(request):
    pass

def logoutView(request):
    pass

def registerView(request):
    template_name = 'authentication/register.html'
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        print(type(f_name), type(l_name), type(username), type(password))
        if len(f_name) == 0 or len(l_name) == 0 or len(username) == 0 or len(password) == 0:
            return render(request, template_name, {'data': dataJSON1})
        if User.objects.filter(username=username):
            return render(request, template_name, {'data': dataJSON2})
        user = User.objects.create_user(username=username, password=password, first_name=f_name, last_name=l_name)
        user.save()
        return redirect('accounts/login')
    else:
        return render(request, template_name, {'data': dataJSON})
