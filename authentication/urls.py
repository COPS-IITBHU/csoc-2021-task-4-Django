from os import name
from django.urls import path
from authentication.views import *

urlpatterns = [
    path('', loginView, name="login-user"),
    path('register', registerView, name="register-user"),
    path('logout', logoutView, name="logout-user"),
    path('changePassword', changePasswordView, name="change-password")
]