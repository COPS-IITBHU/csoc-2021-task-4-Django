from django.urls import path
from store.views import *

urlpatterns = [
    path('', index, name="index"),
    path('books/', bookListView, name="book-list"),
    path('<int:bid>/', bookDetailView, name='book-detail' ),
    path('loaned/', viewLoanedBooks, name="view-loaned"),
    path('loan/', loanBookView, name="loan-book"),
    path('return/', returnBookView, name="return-book"),
]
