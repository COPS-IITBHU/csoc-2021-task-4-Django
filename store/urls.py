from django.urls import path
from store.views import *
from . import views

urlpatterns = [
    path('', index, name="index"),
    path('books/', bookListView, name="book-list"),
    path('book/<int:bid>/', bookDetailView, name='book-detail' ),
    path('books/loaned/', viewLoanedBooks, name="view-loaned"),
    path('books/loan/', loanBookView, name="loan-book"),
    path('books/return/', returnBookView, name="return-book"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('rating', views.handelrating, name="handlerating"),
]
