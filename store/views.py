from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date
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
    bookDetail=Book.objects.get(id=bid)
    available=[a for a in BookCopy.objects.filter(book=bookDetail).filter(status=True)]
    context['book']=bookDetail
    context['num_available']=len(available)
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    bookList=Book.objects.all()
    # START YOUR CODE HERE
    get_data = request.GET
    titleSearch='' if get_data.get('title')==None else get_data.get('title').lower()
    authorSearch='' if get_data.get('author')==None else get_data.get('author').lower()
    genreSearch='' if get_data.get('genre')==None else get_data.get('genre').lower()
    bookList={a for a in bookList if a.title.lower().find(titleSearch)!=-1 and a.author.lower().find(authorSearch)!=-1 and a.genre.lower().find(genreSearch)!=-1}
    context = {
        'books': bookList, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
        'titleSearch':get_data.get('title') or '',
        'authorSearch':get_data.get('author') or '',
        'genreSearch':get_data.get('genre') or '',
    }
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
    # print(request.user)
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
    book_id = int(request.POST['bid']) # get the book id from post data
    bookDetail=Book.objects.filter(id=book_id)[0]
    bookCopies=BookCopy.objects.filter(book=bookDetail).filter(status=True)
    print(bookCopies)
    response_data['message']='success' if len(bookCopies)>0 else 'failure'
    if(len(bookCopies)>0):
        BookCopy.objects.filter(id=bookCopies[0].id).update(borrow_date=date.today(),borrower=request.user,status=False)
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
    # START YOUR CODE HERE
    book_id = int(request.POST['book_id']) # get the book id from post data
    bookCopy=get_object_or_404(BookCopy,id=book_id)
    response_data['message']='success'
    print(type(bookCopy.borrow_date))
    BookCopy.objects.filter(id=book_id).update(borrower=None,status=True)
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': None,
    }
    try:
        book_id = int(request.POST.get('book_id')) # get the book id from post data
        book=Book.objects.filter(id=book_id)
        rating = int(request.POST.get('val'))
        bookPrevRev=bookRating.objects.filter(bookName=book[0]).filter(user=request.user)
        
        if(len(bookPrevRev)==0):
            bookRating.objects.create(bookName=book[0],user=request.user,ratingValue=rating)
        else :
            bookPrevRev.update(ratingValue=rating)
        response_data['message']='success'
        value=0
        bookallRatings=bookRating.objects.filter(bookName=book[0])
        for i in bookallRatings:
            value +=  i.ratingValue
        value=value/len(bookallRatings)
        Book.objects.filter(id=book_id).update(rating=value,ctrating=len(bookallRatings))
    except:
        response_data['message']='failure'
    return JsonResponse(response_data)
