from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def loginView(request):
    pass

def logoutView(request):
    pass

def registerView(request):
    if(request.method == "POST"):
        post_data = request.POST
        username = post_data['username']
        password = post_data['password']
        passConf = post_data['passConf']
        email = post_data['email']
        first_name = post_data['first_name']
        last_name = post_data['last_name']
        if(username and password and email and first_name and last_name):
            if(User.objects.filter(username=username).exists()):
                messages.error(request, 'Username '+ username +' already exists!')
            elif(password == passConf):
                User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user = authenticate(request, username=username, password=password)
                if(user):
                    login(request, user)
                return render(request, 'store/index.html')
            else:
                messages.error(request,'Password did not match')
        else:
            messages.error(request,'Please fill all fields correctly')
    
    return render(request, 'registration/register.html')