from django.urls import path
from authentication.views import *

urlpatterns = [
    path('login/',loginView,name='loginuser'),
    path('logout/',logoutView,name='logoutuser'),
]
