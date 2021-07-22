from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    books = Book.objects.get(id=bid)
    context['book'] = books
    book_num = BookCopy.objects.filter(book = books, status = True)

    context['num_available'] = len(book_num)
    
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

    book_list = Book.objects.all()

    if get_data.get('title') != None:
        book_list = book_list.filter(title__icontains=get_data.get('title'))
    
    if get_data.get('author') != None:   
        book_list = book_list.filter(author__icontains=get_data.get('author'))
        
    if get_data.get('genre') != None:
        book_list = book_list.filter(genre__icontains=get_data.get('genre'))
               
    context['books'] = book_list
    
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
    loaned_book = BookCopy.objects.filter(borrower = request.user)
    context['books'] = loaned_book
    
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
    book_id = request.POST.get('bid')

    books = Book.objects.get(id=book_id)
    book_copy = BookCopy.objects.filter(book = books)
    response_data['message'] = 'failure'
    for x in book_copy:
        if x.status == True:
            response_data['message'] = 'success'
            book_copy[0].borrower = request.user
            book_copy[0].borrow_date = datetime.today()
            book_copy[0].status = False
            book_copy[0].save()

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
   
    book_id = request.POST.get('bid')

    try:
        book_copy = BookCopy.objects.get(id=book_id)
        response_data['message'] = 'success'
        book_copy.borrower = None
        book_copy.borrow_date = None
        book_copy.status = True
        book_copy.save()
    except:
        response_data['message'] = 'failure'
        

    return JsonResponse(response_data)


@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': None,
    }

    if request.POST:
        book_id = request.POST.get('bid')
        book_rate = request.POST.get('brate')

        books = Book.objects.get(id=book_id)
        rating1 = BookRating.objects.filter(book=books, user=request.user)

        if len(rating1)==0:
            new_rating = BookRating(book=books, user=request.user, rating=book_rate)
            new_rating.save()
        else:
            for i in rating1:
                i.rating = book_rate
                i.save()

        Calc_Rate=BookRating.objects.filter(book=books)
        book_rate = 0
        for r in Calc_Rate:
            book_rate +=  r.rating
        book_rate /= len(Calc_Rate)
        book_rate = round(book_rate,2)

        Book.objects.filter(id=book_id).update(rating=book_rate)
        response_data['message']='success'
        

    else:
        response_data['message']='failure'

    return JsonResponse(response_data)