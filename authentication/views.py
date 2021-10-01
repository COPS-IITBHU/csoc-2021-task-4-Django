# from django.shortcuts import render,request,redirect
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def loginView(request):
      if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully!")
            return redirect('/')

        elif (username == "") or (password == ""):
            messages.error(request,"Empty field/s!")
            return render(request, 'authentication/login.html')

        else:
            messages.error(request,"User credentials are incorrect!")
            return render(request, 'authentication/login.html')

      else:
        return render(request, 'authentication/login.html')

def logoutView(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('/')

def registerView(request):
     if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        print(firstname , lastname, password , username, email)

        if (firstname == "") or (lastname == "") or (username == "") or (email == "") or (password == "") or (confirmpassword == ""):
            messages.error(request,"Empty field/s!")
            return render(request, 'authentication/register.html')

        elif (confirmpassword != password):
            messages.error(request,"Passwords do not match!")
            return render(request, 'authentication/register.html')

        elif User.objects.filter(username = username).exists():
            messages.error(request,"Username already taken!")
            return render(request, 'authentication/register.html')

        elif (User.objects.filter(email = email).exists()):
            messages.error(request,"Email address already taken!")
            return render(request, 'authentication/register.html')

        else:

            user = User.objects.create_user(username,email,password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            login(request,user)
            messages.success(request,"Account successfully created!")
            return redirect('/')

     else:        
        return render(request, 'authentication/register.html')

def changePasswordView(request):
    if request.method == "POST":
        newPassword = request.POST.get('newPassword')
        confirmNewPassword = request.POST.get('confirmNewPassword')
        email = request.POST.get('email')
        user = None

        if (newPassword == "") or (confirmNewPassword == "") or (email == ""):
            messages.error(request,"Empty field/s!")
            return render(request,'authentication/changePassword.html')

        elif (newPassword != confirmNewPassword):
            messages.error(request,"Passwords do not match!")
            return render(request,'authentication/changePassword.html')

        elif not User.objects.filter(email = email).exists():
            messages.error(request,"Email address is wrong!")
            return render(request,'authentication/changePassword.html')

        else:
            user = User.objects.get(email = email)
            user.set_password(newPassword)
            user.save()
            return redirect('/userAccount/') 
    else:           
        return render(request,'authentication/changePassword.html') 
