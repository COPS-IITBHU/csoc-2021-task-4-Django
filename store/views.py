from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    book = get_object_or_404(Book, id=bid)
    bookcopy = get_object_or_404(BookCopy, book=book)

    context['book'] = book

    if book.is_available:
        context['num_available'] = len(bookcopy)
    else:
        context['num_available'] = 0
    
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
    var = Book.objects.filter(title__icontains=get_data.get('title',''), author__icontains=get_data.get('author',''), genre__icontains=get_data.get('genre',''))

    context['books'] = var
    
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
    user = request.user
    loanedBookCopy = BookCopy.objects.filter(borrower=user)

    context['books'] = loanedBookCopy

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
    book = get_object_or_404(Book, id=request.POST.get('book_id'))
    if book.is_available:
        user = request.user
        bookCopy = BookCopy.objects.get(book=book, borrower=None)
        bookCopy.borrower = user
        bookCopy.save()
        response_data['message'] = 'success'
    else:
        response_data['message'] = 'failure'

    book_id = None # get the book id from post data


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
    pass


