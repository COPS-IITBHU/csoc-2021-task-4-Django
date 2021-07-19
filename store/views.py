from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# from django.contrib.auth.models import User
# from django.contrib.auth import logout, authenticate, login
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': 0, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    get_data = request.GET
    # START YOUR CODE HERE
    context['book'] = Book.objects.filter(pk=bid)[0]
    available=0
    copies=BookCopy.objects.filter(book=context['book'])
    for i in range(len(copies)):
        if ((copies[i].__str__()).find('Available')!=-1): available=available+1
    context['num_available'] = available
    # print(BookCopy.objects.filter(book=context['book'])[2])
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    books = Book.objects.all()
    if(get_data.get('title')): books=books.filter(title=get_data.get('title'))
    if(get_data.get('author')): books=books.filter(author=get_data.get('author'))
    if(get_data.get('genre')): books=books.filter(genre=get_data.get('genre'))
    context['books']=books
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    context['books'] = BookCopy.objects.filter(borrower=request.user)
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = request.POST.get('bid') # get the book id from post data
    book = Book.objects.filter(pk=book_id)[0]
    bookcopy=BookCopy.objects.filter(book=book).filter(status=True)
    if (len(bookcopy)):
        bookcopy=bookcopy[0] 
        if(len(BookRating.objects.filter(book=book,rater=request.user.username))==0):
            issuedbook = BookRating(book=book,rater=request.user.username)
            issuedbook.save()
        response_data['message'] = 'success'
        bookcopy.borrower=request.user
        bookcopy.borrow_date=datetime.today()
        bookcopy.status=False
        bookcopy.save()
    else: response_data['message'] = 'failure'
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    response_data = {
        'message': "Book is successfully returned! Watch for more books.",
    }
    book_id = request.POST.get('bid') # get the book id from post data
    book = Book.objects.filter(pk=book_id)[0]
    bookcopy=BookCopy.objects.filter(book=book).filter(status=False)[0] 
    bookcopy.borrower=None
    bookcopy.borrow_date=None
    bookcopy.status=True
    bookcopy.save()
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBook(request):
    response_data = {
        'message': "Successfully rated!",
    }
    username =request.user.username
    book_id = request.POST.get('bid') # get the book id from post data
    book = Book.objects.filter(pk=book_id)[0]
    newrating = BookRating.objects.filter(book=book,rater=username)
    if(len(newrating)==0):
        response_data['message']="You have not issued the book!"
        return JsonResponse(response_data)
    newrating=newrating[0]
    rate = request.POST.get('rate')
    newrating.rated=True
    newrating.rating=rate
    newrating.save()

    bookratings=BookRating.objects.filter(book=book,rated=True)
    sum=0.0
    for i in range(len(bookratings)):
        sum=sum+bookratings[i].rating
    book.rating=(float)(sum/len(bookratings))
    book.save()
    return JsonResponse(response_data)