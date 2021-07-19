from django.urls import path
from store.views import *

urlpatterns = [
    # urlpatterns here 
    path('', index, name="index"),
    path('books/', bookListView, name="book-list"),
    path('books/return/', returnBookView, name="return-book"),
    path('books/loan/', loanBookView, name="loan-book"),
    path('book/<int:bid>/', bookDetailView, name='book-detail' ),
    path('books/loaned/', viewLoanedBooks, name="view-loaned"),
    path('books/userrating/', rateBookView, name="rate-book"),
]
