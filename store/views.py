from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from datetime import date
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None,
        'num_available': None,
    }   
    book = get_object_or_404(Book, pk=bid)
    bookcopy = get_list_or_404(BookCopy, book=bid)
    context['book'] = book
    context['num_available'] = len(bookcopy)
    return render(request, template_name, context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,
    }
    get_data = request.GET
   
    var = Book.objects.filter(title__icontains=get_data.get('title',''),author__icontains=get_data.get('author',''),genre__icontains=get_data.get('genre', ''))

    context['books'] = var
    return render(request, template_name, context=context)

@login_required
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
            response_data['message'] = 'failiure'
    


    return JsonResponse(response_data)


@csrf_exempt
@login_required
def returnBookView(request):
     response_data = {
        'message': None,
    }
     if request.method == 'POST':
        bid = request.POST['id']
        try:
            bookcopy = BookCopy.objects.get(pk=bid)
        except:
            return JsonResponse({'message':'No such book'})  

        else:
            bookcopy.status = True
            bookcopy.borrower = None
            bookcopy.borrow_date = None
            bookcopy.save()
            return JsonResponse({'message':'success'})
          

@csrf_exempt
@login_required
def rateBookView(request):
    
    response_data = {
        'message': None,
    }
    if request.method == "POST":
        data = request.POST
        bid=data.get('bid','')
        rate=data.get('rate',0.0)
        book = Book.objects.get(pk=bid)
        book.rate = rate

        prevrating=BookRating.objects.filter(user=request.user,book=book)
        rating=BookRating()
        rating.book=book
        rating.user=request.user
        rating.rating=rate
        prevrating.delete()
        rating.save()
        other=BookRating.objects.filter(book=book)
        rating_total = 0.0

        for r in other:
            rating_total += r.rating
        
        book.rating = rating_total/len(other)
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


