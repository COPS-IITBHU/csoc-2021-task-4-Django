from django.shortcuts import render
from django.shortcuts import get_object_or_404,get_list_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Avg

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
        'book_allRatings': None,
    }
    # START YOUR CODE HERE
    book = get_object_or_404(Book, pk=bid)
    bookAvail = BookCopy.objects.filter(book__pk=bid,status=True).count()
    context['book'] = book
    context['num_available'] = bookAvail
    context['book_allRatings'] = BookRating.objects.filter(book__pk=bid)[:3]
    
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
    bl = Book.objects.all()
    if(get_data):
        btitle = get_data['title']
        bauthor = get_data['author']
        bgenre = get_data['genre']
        
        if(btitle):
            bl = bl.filter(title=btitle)
        if(bauthor):
            bl = bl.filter(author=bauthor)
        if(bgenre):
            bl = bl.filter(genre__icontains=bgenre)

    context['books'] = bl
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
    context['books'] = BookCopy.objects.filter(status=False, borrower=request.user)


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
    post_data = request.POST
    book_id = post_data['bid'] # get the book id from post data
    bookAvail = BookCopy.objects.filter(book__pk=book_id,status=True)[0]
    if(not bookAvail):
        response_data['message']="failure"
    else:
        BookCopy.objects.filter(pk = bookAvail.id).update(borrow_date= datetime.date.today(), status=False, borrower= request.user)
        response_data['message']="success"

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
    post_data = request.POST
    book_id = post_data['bid']
    bookAvail = BookCopy.objects.filter(pk=book_id)
    if(not bookAvail):
        response_data['message']="failure"
    else:
        bookAvail.update(borrow_date= None, status=True, borrower= None)
        response_data['message']="success"
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': "success",
    }
    post_data = request.POST
    book_id = post_data['bid']
    rating = float(post_data['rating'])
    desc = post_data['desc']
    if(rating < 0 or rating > 10):
        response_data['message'] = "failure"
    else:     
        ratedBook = BookRating.objects.filter(book__pk=book_id, ratedBy=request.user)
        book = Book.objects.get(pk=book_id)

        if(ratedBook):
            ratedBook.update(rating=rating,desc=desc)
        if(not ratedBook):
            BookRating.objects.create(book=book, ratedBy=request.user, rating=rating, desc=desc)

        avgRating = BookRating.objects.filter(book__pk=book_id).aggregate(Avg('rating'))['rating__avg']
        avgRating = round(float(avgRating),2)
        Book.objects.filter(pk=book_id).update(rating=avgRating)

    return JsonResponse(response_data)