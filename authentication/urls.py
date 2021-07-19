from django.urls import path
from authentication.views import *

urlpatterns = [
    path("login/", loginView, name="loginView"),
    path("register/", registerView, name="register"),
    path("logout/", logoutView, name="logout"),
]