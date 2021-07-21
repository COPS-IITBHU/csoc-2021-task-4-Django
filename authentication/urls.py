from django.urls import path
from authentication.views import *

urlpatterns = [
    # setting the paths for the Library App
    
    path('login/',loginView, name='loginView'),
    path('logout/',logoutView, name='logoutView'),
    path('register/',registerView, name='registerView'),
    # path(r'^404',"website.views.page_404",name='page_404'),
    # path('check/',home,name='home'),
    # checking the path here 

]