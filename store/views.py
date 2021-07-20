from django.shortcuts import render
from django.utils import timezone
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
        'book': None,  # set this to an instance of the required book
        # set this to the number of copies of the book available, or 0 if the book isn't available
        'num_available': None,
    }
    # START YOUR CODE HERE
    book = get_object_or_404(Book, id=bid)
    context['book'] = book
    context['num_available'] = len(BookCopy.objects.filter(book=book, status=True))
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,  # set this to the list of required books upon filtering using the GET parameters
        # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    if get_data:
        context['books'] = Book.objects.filter(title__icontains=get_data['title'], author__icontains=get_data['author'], genre__icontains=get_data['genre'])
    else:
        context['books'] = Book.objects.all()

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
    books = BookCopy.objects.filter(borrower=user)
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
    
    bid = request.body.decode("utf-8").split("=")[1]
    Mbook=Book.objects.filter(id=bid)
    book = BookCopy.objects.filter(book=Mbook[0], status=True)[0]

    if book:
        book.borrower = request.user
        book.borrow_date = timezone.datetime.today().date()
        book.status = False
        book.save()
        response_data['message'] = 'success'
    else:
        response_data['message'] = 'failure'
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

    bid = request.body.decode("utf-8").split("=")[1]
    book = BookCopy.objects.get(id=bid)

    if book:
        book.borrower = None
        book.borrow_date = None
        book.status = True
        book.save()
        response_data['message'] = 'success'
    else:
        response_data['message'] = 'failure'
    return JsonResponse(response_data)

def rateBookView(request,bid):
    print(bid)
    template_name = 'store/book_list.html'
    context = {
        'books': None,  # set this to the list of required books upon filtering using the GET parameters
        # (i.e. the book search feature will also be implemented in this view)
    }
    rating = float(request.POST.get('rating'))
    book = get_object_or_404(Book, id=bid)
    try:
        book_rating = BRating.objects.get(critic=request.user,book=book)
        book_rating.rating=rating
        book_rating.save()
    except:
        BRating.objects.create(critic=request.user,book=book,rating=rating)
    
    all_ratings=BRating.objects.filter(book=book)
    final_rating=0
    n=0
    for i in all_ratings:
        final_rating+=i.rating
        n+=1
    final_rating/=n
    Book.objects.filter(id=bid).update(rating=final_rating)

    context['books'] = Book.objects.all()
    return render(request, template_name, context=context)