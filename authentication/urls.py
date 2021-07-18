from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]