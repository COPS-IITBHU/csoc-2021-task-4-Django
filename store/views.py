from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal


# Create your views here.

def index(request):
    return render(request, 'store/index.html')


def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    try:
        book = Book.objects.get(pk=bid)
    except:
        raise Http404('No such book!')
    else: 
        num_available = BookCopy.objects.filter(book__exact=book,
        status__exact=True).count()
        context = {
        'book': book, 
        'num_available': num_available, 
        }
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    books = Book.objects.filter(
        title__icontains = get_data.get('title',''),
        author__icontains = get_data.get('author',''),
        genre__icontains = get_data.get('genre',''),
    )
    context = {
        'books': books, 
    }
    return render(request, template_name, context=context)



@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books = BookCopy.objects.filter(borrower__exact=request.user)
    context = {
        'books': books,
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
    if request.method == 'POST':
        bid = request.POST.get('bid', None)
        bookcopy = BookCopy.objects.filter(book=bid, status=True)
        if len(bookcopy) > 0:
            bookcopy[0].borrower = request.user
            bookcopy[0].borrower_date = date.today()
            bookcopy[0].status = False
            bookcopy[0].save()
            response_data['message'] = 'success'
        else:
            response_data['message'] = 'not available'
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
 if request.method == 'POST':
        book_id = request.POST['id']
        try:
            book = BookCopy.objects.get(pk=book_id)
        except:
            return JsonResponse({'message':'No such book'})  

        else:
            book.status = True
            book.borrower = None
            book.borrow_date = None
            book.save()
            return JsonResponse({'message':'success'})



@csrf_exempt
@login_required
def rateBookView(request):
    if request.method == "POST":
        bid = request.POST['bid']
        change_rating = Decimal(request.POST['rating'])
        if change_rating >= 0 and change_rating <= 10:
            try:
                book = Book.objects.get(pk=bid)
                user = User.objects.get(username = request.user.username)
                old_rating = BookRating.objects.filter(book = book, user = user)
                old_rating.delete()
                objt = BookRating()
                objt.user = user
                objt.book = book
                objt.rate = change_rating
                objt.save()
                books = BookRating.objects.filter(book = book)
                total = 0
                for i in books:
                    total+=i.rate
                book.rating = total/books.count()
                book.save()
            except:
                return JsonResponse({'message':"error"})
            else:
                return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message':'Rate from 0-10'})

   
