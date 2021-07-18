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
        'book': Book.objects.get(id=bid), # set this to an instance of the required book
        'num_available': len(BookCopy.objects.filter(book=bid, status=True).all()), # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'

    title = request.GET.get('title') or ''
    author = request.GET.get('author') or ''
    genre = request.GET.get('genre') or ''

    context = {
        # set this to the list of required books upon filtering using the GET parameters
        'books': Book.objects.filter(title__contains=title, author__contains=author, genre__contains=genre).all(),
                       # (i.e. the book search feature will also be implemented in this view)
    }
    return render(request, template_name, context=context)

@login_required()
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    books = BookCopy.objects.filter(borrower=request.user).all()
    context['books'] = books

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
    book = Book.objects.get(id = book_id)

    available_copies = BookCopy.objects.filter(book=book, status=True).all()
    if (len(available_copies) > 0) :
        response_data['message'] = "success"
        issued = available_copies[0]
        issued.status = False
        issued.borrow_date = datetime.now()
        issued.borrower = request.user
        issued.save();
    else :
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
        'message' : 'failure',
    }

    copy_id = request.POST.get('bid')
    copy = BookCopy.objects.get(id = copy_id)
    copy.status = True
    copy.borrower = None
    copy.borrow_date = None
    copy.save();

    response_data['message'] = 'success'
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request, bid) :
    if (request.method == 'POST') :
        rating = int(request.POST.get('rating'))
        book = Book.objects.get(id=bid)
        
        if (Ratings.objects.filter(book=book, user=request.user).exists()) :
            ratedBy = len(Ratings.objects.filter(book=book).all())
            prevRating = Ratings.objects.get(book=book, user=request.user)
            newRating = (ratedBy*book.rating-prevRating.rating+rating)/ratedBy
            newRating = round(newRating, 1)

            prevRating.rating = rating
            book.rating = newRating
            prevRating.save();
            book.save();

        else :
            ratedBy = len(Ratings.objects.filter(book=book).all())
            newRating = (ratedBy*book.rating+rating)/(ratedBy+1)
            newRating = round(newRating, 1)

            ratingValue = Ratings(book=book, user=request.user, rating=rating)
            book.rating = newRating
            ratingValue.save();
            book.save();

        return redirect(f'/book/{bid}/')
    return redirect(f'/book/{bid}/')
