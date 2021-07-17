from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from store.models import *
from django.shortcuts import get_object_or_404
from datetime import date
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.views.decorators.csrf import csrf_exempt


# index function 
def index(request):
    return render(request, 'store/index.html')

# bookDetailView function 
def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None,
        'num_available': None,
    }   
    
    book = get_object_or_404(Book,pk=bid)
    bookcopy = get_list_or_404(BookCopy, book=bid, status=True)

    context['book']=book
    context['num_available']=len(bookcopy)

    return render(request, template_name, context=context)


@csrf_exempt
# bookListView function
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,
    }
    get_data = request.GET
   
    query = Book.objects.filter(title__icontains=get_data.get('title',''),author__icontains=get_data.get('author',''),genre__icontains=get_data.get('genre', ''))

    context['books'] = query
    return render(request, template_name, context=context)

@login_required
# viewLoanedBooks function for the borrowed books
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }

    
    loanedbookcopy =  BookCopy.objects.filter(borrower=request.user)
    context['books'] = loanedbookcopy
    return render(request, template_name, context=context)

@csrf_exempt
@login_required


# loaned or borrowed book function as loanBookView
def loanBookView(request):
    response_data = {
        'message': None,
    }
    
    data = request.POST
    if request.method=='POST':
        bid = data.get('bid','')
    book_id = bid 

    bookcopy = BookCopy.objects.filter(book=book_id,status=True)

    if len(bookcopy)==0:
        response_data['message'] = 'failure'
    else:    
        bookcopy[0].borrower = request.user
        bookcopy[0].borrow_date = date.today()
        bookcopy[0].status = False
        bookcopy[0].save()
        response_data['message'] = 'success'

    return JsonResponse(response_data)


@csrf_exempt
@login_required

# function for returning the book 
def returnBookView(request):
    response_data = {
        'message': None,
    }

    data = request.POST
    if request.method=='POST':
        bid = data.get('bid','')
    book_id = bid 

    print ("CONSOLE LOG")
    bookcopy = BookCopy.objects.filter(pk=book_id)

    if len(bookcopy)==0:
        response_data['message'] = 'failure'
    else:    
        bookcopy[0].borrower = None
        bookcopy[0].borrow_date = None
        bookcopy[0].status = True
        bookcopy[0].save()
        response_data['message'] = 'success'

    return JsonResponse(response_data)

@csrf_exempt
@login_required

# function for rating the book
def rateBookView(request):
    
    if request.method == "POST":
        data = request.POST
        bid=data.get('bid','')
        rate=data.get('rate',0.0)
        print(bid)
        print(rate)
        book = Book.objects.get(pk=bid)
        oldRating=UserRating.objects.filter(user=request.user,book=book)
        rating=UserRating()
        rating.book=book
        rating.user=request.user
        rating.rating=rate
        oldRating.delete()
        rating.save()
        other=UserRating.objects.filter(book=book)
        rating_sum = 0.0
        for current in other:
            rating_sum += current.rating
        book.rating = rating_sum/other.count()
        book.rating = round(book.rating,2)
        book.save()
        response_data={
            'message':'success'
        }
    else:
        response_data={
            'message':'failure'
        }
    return JsonResponse(response_data)




