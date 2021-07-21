from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

@csrf_exempt
def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    book=get_object_or_404(Book,id=bid)
    context['num_available'] =BookCopy.objects.filter(book=book,status=True).count()
    context['book']=book
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
    if get_data:
        context['books']=Book.objects.filter(title__icontains=get_data['title'],author__icontains=get_data['author'],genre__icontains=get_data['genre'])
    else:
        context['books']=Book.objects.all()
    
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
    context['books']=BookCopy.objects.filter(borrower=request.user)
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
    book=BookCopy.objects.filter(book=Book.objects.filter(id=request.POST['bid'])[0],status=True)[0]

    if book:
        book.borrow_date = datetime.today().date()
        book.status = False
        book.borrower = request.user
        book.save()
        response_data['message']='success'
    else:
        response_data['message']='failure'

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
    book=BookCopy.objects.get(id=request.POST['bid'])
    if book:
        book.borrow_date = None
        book.status = True
        book.borrower = None
        book.save()
        response_data['message']='success'
    else:
        response_data['message']='failure'

    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBook(request):
    response_data = {
        'message': None,
    }
    # START YOUR CODE HERE
    book_id = None # get the book id from post data
    book=Book.objects.filter(id=request.POST['bid'])
    if book:
        boo_k=Book.objects.filter(id=request.POST['bid'])[0]
        try:
            ratingbook=BookRate.objects.filter(book_rated=boo_k)[0]
            num=boo_k.total_rated
            boo_k.rating=(num*(boo_k.rating)-ratingbook.user_rating+int(request.POST['rating']))/num
            boo_k.save()
            ratingbook.user_rating=int(request.POST['rating'])
            ratingbook.save()
        except:
            num=boo_k.total_rated
            boo_k.rating=(num*(boo_k.rating)+int(request.POST['rating']))/(num+1)
            boo_k.save()
            BookRate.objects.create(book_rated=boo_k,user_name=request.user,user_rating=int(request.POST['rating']))
            boo_k.total_rated+=1
        response_data['message']='success'
    else:
        response_data['message']='failure'

    return JsonResponse(response_data)
