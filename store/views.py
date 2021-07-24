from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

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
    try:
        context['book'] = Book.objects.get(pk=bid)
        context['num_available'] = len(BookCopy.objects.filter(book=context['book']).filter(status=True))
    except Book.DoesNotExist:
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

    get_data = request.GET
    filteredBooks = Book.objects.all()
    if 'author' in get_data:
        if len(get_data['author']) != 0:
            filteredBooks = filteredBooks.filter(author=get_data['author'])
    if 'genre' in get_data:
        if len(get_data['genre']) != 0:
            filteredBooks = filteredBooks.filter(genre=get_data['genre'])
    if 'title' in get_data:
        if len(get_data['title']) != 0:
            filteredBooks = filteredBooks.filter(title=get_data['title'])        
    context['books'] = filteredBooks
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
    bookCopys = BookCopy.objects.all()
    loanedByUser = []
    user = request.user
    for bookCopy in bookCopys:
        if(bookCopy.borrower) == user:
            loanedByUser.append(bookCopy)
            
    context['books'] = loanedByUser        

    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    # get the book id from post data
    response_data = {
        'message': 'failure',
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # # START YOUR CODE HERE
    # bId = request.POST['bid'] # get the book id from post data
    # book = Book.objects.get(pk=bId)
    # if book.num_avail > 0:
    #     response_data['message'] = 'success'
    # return JsonResponse(response_data)
    book_id = int(request.POST['bid']) # get the book id from post data
    book=Book.objects.filter(id=book_id)[0]
    bookCopy=BookCopy.objects.filter(book=book).filter(status=True)
    if len(bookCopy)>0:
        response_data['message']='success'
        BookCopy.objects.filter(id=bookCopy[0].id).update(borrow_date=date.today(),borrower=request.user,status=False)
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
        'message': 'failure',
    }
    bId = int(request.POST['book_id']) 
    BookCopy.objects.filter(id=bId).update(borrower=None,status=True,borrow_date=None)
    response_data['message']='success'
    return JsonResponse(response_data)


