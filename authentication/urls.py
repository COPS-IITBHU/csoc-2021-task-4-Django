from django.urls import path, include
from authentication.views import *

urlpatterns = [
    path('accounts/login/', loginView, name="login"),
    path('register/', registerView, name="register"),
    path('log-out/', logoutView, name="log-out"),
]