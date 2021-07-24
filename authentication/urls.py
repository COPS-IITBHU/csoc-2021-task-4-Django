from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/', registerView, name='register'),
]