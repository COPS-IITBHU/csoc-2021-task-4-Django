from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': Book.objects.filter(id=bid).first(), 
        'num_available': BookCopy.objects.filter(book__id=bid, status=True).count, 
    }
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    title = request.GET.get('title')
    author = request.GET.get('author')
    genre = request.GET.get('genre')

    books = Book.objects.all()
    variables = {'title':title, 'author':author, 'genre':genre}
    for key, value in variables.items():
        if key=='title' and value:
            books = books.filter(title__icontains=value)
        if key=='author' and value:
            books = books.filter(author__icontains=value)
        if key=='genre' and value:
            books = books.filter(genre__icontains=value)

    context = {
        'books': books, 
    }
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': BookCopy.objects.filter(borrower = request.user),
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    
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
    num_copies = BookCopy.objects.filter(book__id=book_id, status=True).count()

    if not request.user.is_authenticated:
        response_data['message'] = "failure" 
        return JsonResponse(response_data)
    
    if(num_copies):
        loan_copy = BookCopy.objects.filter(book__id=book_id, status=True).first()
        loan_copy.status = False
        loan_copy.borrow_date = datetime.today()
        loan_copy.borrower = request.user
        loan_copy.save()
        response_data['message'] = "success"
    else:
        response_data['message'] = "failure"    
    
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
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    bid = request.POST.get('bid')
    loan_copy = BookCopy.objects.all()[int(bid)-1]
    
    loan_copy.status = True
    loan_copy.borrow_date = None
    loan_copy.borrower = None
    loan_copy.save()
    response_data['message'] = "success"
    
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    bid = request.POST.get('bid')
    rating = request.POST.get('rating')
    print(rating)

    book = Book.objects.filter(id=bid).first()
    user = request.user
    rating_data = RatingSystem.objects.filter(book=book,rated_by=user).first()
    if(rating_data):
        rating_data.rating = rating
        rating_data.save()
    else:
        rate = RatingSystem.objects.create(book=book, rated_by=user, rating=rating)

    totalrating = 0
    for ratings_multi in RatingSystem.objects.filter(book=book):
        totalrating += ratings_multi.rating
    book.rating = totalrating/RatingSystem.objects.filter(book=book).count()
    book.save()
    
    response_data['message'] = "success"
    
    return JsonResponse(response_data)
