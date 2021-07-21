from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def indexView(request):
    return render(request,'home.html')

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
            form = UserCreationForm()
    return render(request,'register.html', { 'form': form })
    