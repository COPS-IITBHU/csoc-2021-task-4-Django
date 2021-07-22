from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),
    path('login/', loginView, name='login'),
] 