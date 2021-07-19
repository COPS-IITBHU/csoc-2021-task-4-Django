from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# SignUpForm class 
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=200)

# meta class 
class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )