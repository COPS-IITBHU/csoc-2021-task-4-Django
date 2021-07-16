from django.urls import path,include
from store.views import *

urlpatterns = [
    path('', index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('books/', bookListView, name="book-list"),
    path('book/<int:bid>/', bookDetailView, name='book-detail' ),
    path('books/loaned/', viewLoanedBooks, name="view-loaned"),
    path('books/loan/', loanBookView, name="loan-book"),
    path('books/rate/', rateBookView, name="rate-book"),
    path('books/return/', returnBookView, name="return-book"),
]