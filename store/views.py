from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import re
 
from django.db.models import Q
 

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    context['book'] = Book.objects.get(id__exact=bid)
    list = BookCopy.objects.filter(Q(book=Book.objects.get(id__exact=bid)) & Q(available=True))
    count = list.count()
    context['num_available'] = count
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    print(get_data)
    # START YOUR CODE HERE
    # <QueryDict: {'title': ['chemisty'], 'author': ['o p tandon'], 'genre': ['science chemistry']}>
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')
    print(title)
    print(author)
    print(genre)
    # fileredList1 = Book.objects.filter(title__icontains=title)
    # fileredList2 = fileredList1.objects.filter(author__icontains=author)
    # fileredList3 = fileredList2.objects.filter(genre__icontains=genre)
    # context['books']= fileredList3
    # options = {}
    # for key in ('title', 'author', 'genre'):
    #     value = request.GET.get(key)
    #     if value:
    #         options[key] = value
    # context['books'] = Book.objects.filter(**options)

    context['books'] = Book.objects.filter(
            Q(title__icontains=title) & Q(author__icontains=author) & Q(genre__icontains=genre))
    # context['books']= Book.objects.filter(get_data)
    
    
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


