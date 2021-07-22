from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, response
from datetime import datetime
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
    context['book']=Book.objects.get(id=bid)
    context['num_available']=len(BookCopy.objects.filter(book=bid, status=True).all())
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    # START YOUR CODE HERE
    bookList=Book.objects.all()
    authorName=''
    title=''
    genre=''
    if(request.GET.get('title')) : authorName=request.GET.get('title')
    if(request.GET.get('author')) : title=request.GET.get('author')
    if(request.GET.get('genre')) : genre=request.GET.get('genre')
    context['books']=bookList.filter(title__icontains=title,author__icontains=authorName,genre__icontains=genre)

    
    
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
    book_id = request.POST.get('bid') # get the book id from post data
    bookcopy = BookCopy.objects.filter(book=book_id,status=True)
    if (len(bookcopy) > 0) :
        issue_book = bookcopy[0]
        issue_book.status = False
        issue_book.borrow_date = datetime.today()
        issue_book.borrower = request.user
        issue_book.save()
        response_data['message'] = "success"
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
        'message': None,
    }
    book_id = request.POST.get('bid') # get the book id from post data
    bookcopy=BookCopy.objects.filter(pk=book_id,status=False) 
    if (len(bookcopy) > 0) :
        issue_book = bookcopy.first()
        response_data['message'] = "success"
        issue_book.status = True
        issue_book.borrow_date = None
        issue_book.borrower = None
        issue_book.save()
    else :
        response_data['message'] = "failure"    
    
        

    return JsonResponse(response_data)


@csrf_exempt
@login_required
def rateBookView(request,bid):
    template_name = 'store/book_list.html'
    response_data = {
        'message': "Book has been Successfully Rated!",
    }
    if request.method=="POST":
        data = request.POST
        rating = data.get('rating')
        book = Book.objects.get(pk=bid)
        try:
            bookrating = BookRating.objects.get(rater=request.user,book=book)
            bookrating.rating=rating
            bookrating.save()
        except:
            BookRating.objects.create(rater=request.user,book=book,rating=rating)

        ratebook=BookRating.objects.filter(book=book)
        updatedsum=0
        
        for i in ratebook:
            updatedsum+=i.rating
            
        updatedsum=round((float)(updatedsum/len(ratebook)), 2)

        bookrate=Book.objects.get(pk=bid)
        bookrate.rating=updatedsum 
        bookrate.save()
        
    else:
        response_data = {
        'message': "Error encountered"
    }
    
    return render(request, template_name) 




