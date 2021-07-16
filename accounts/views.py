from django.shortcuts import render
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.views.generic import CreateView
# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'