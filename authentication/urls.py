from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/',registerView,name='registeruser'),
    path('',loginView,name='loginuser'),
    path('logout/',logoutView,name='logoutuser'),
    path('registerform/',registerform,name='registerform'),
]
