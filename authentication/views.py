# from django.shortcuts import render,render_to_response,redirect
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirectBase
from django.core.checks import messages
from django.template import RequestContext
from library.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


# Create your views here.

# loginView function
def loginView(request):
    if request.method == 'GET':
        return render(request,'authentication/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'authentication/login.html',{'form':AuthenticationForm(),'error':'Username and Password did not match.'})
        else:
            login(request,user)
            return redirect('index')

# logoutView function
def logoutView(request):
    return redirect('index')

# registerView function
def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})

# def home(request):
#     return HttpResponse ("home check")
# checking the working of the function and the path 

# def page_404(request):
#     return render_to_response('404.html', RequestContext(request))
