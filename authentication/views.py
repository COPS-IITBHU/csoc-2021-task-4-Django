from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def loginView(request):
    response_data = {
        'message': None,
    }
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        response_data['message'] = "failure" 
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response_data['message'] = "success" 
                return JsonResponse(response_data)
        return JsonResponse(response_data)   

    return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return render(request, 'logout.html')

@csrf_exempt
def registerView(request):
    if request.method=="POST":
        firstname = request.POST.get('firstname') 
        lastname = request.POST.get('lastname') 
        email = request.POST.get('email') 
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

    return render(request,'register.html')