from django.db.models.fields import NullBooleanField
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



def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
        'RatingByLoggedInUser': None,
    }
    # START YOUR CODE HERE
    b = Book.objects.get(id = bid)
    
          # update rating of the book in the Book model
    Ratings = [x for x in RatingOfBook.objects.filter(book = b)]
    l = len(Ratings)
    sum = 0

    if(l != 0 ):
        for r in Ratings:
            sum = sum + r.ratingValue

        avg = sum/l
    else:
        avg = 0    
    b.rating = avg
    b.save()

    context['book'] = b
    if request.user.is_authenticated:
        r = RatingOfBook.objects.filter(book = b, userWhoRated = request.user)
        if r:
            for x in r:
                context['RatingByLoggedInUser'] = x.ratingValue
    
    AllCopies = [x for x in BookCopy.objects.filter(book = b, status = True)]
    context['num_available'] = len(AllCopies)
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
    Title = get_data.get('title',"").strip()
    Author = get_data.get('author',"").strip()
    Genre = get_data.get('genre',"").strip()
    if get_data:
        if (Title != "" and Author != "" and Genre != ""):
            b = Book.objects.filter(title__contains = Title,author__contains = Author, genre__contains = Genre)
        
        elif (Title != "" and Author != ""):
            b = Book.objects.filter(title__contains = Title,author__contains = Author)

        elif (Title != "" and Genre != ""):
            b = Book.objects.filter(title__contains = Title, genre__contains = Genre)

        elif (Genre != "" and Author != ""):
            b = Book.objects.filter(author__contains = Author, genre__contains = Genre)

        elif (Title != ""):
            b = Book.objects.filter(title__contains = Title)

        elif (Author != ""):
            b = Book.objects.filter(author__contains = Author)

        elif (Genre != ""):
            b = Book.objects.filter(genre__contains = Genre)

        else:
            b = Book.objects.all()
        
    else:
        b = Book.objects.all()

    
    print("yahoo")
  # update rating of the book in the Book model
    AllBooks = [x for x in Book.objects.all()]
    for bookk in AllBooks:
        Ratings = [x for x in RatingOfBook.objects.filter(book = bookk)]
        l = len(Ratings)
        sum = 0

        if(l != 0):
            for r in Ratings:
                sum = sum + r.ratingValue

            average_rating = sum/l
        else:
            average_rating = 0    
        bookk.rating = average_rating
        bookk.save() 

    context['books'] = b
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
    context['books'] = [x for x in BookCopy.objects.filter(borrower = request.user, status = False)]

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
    if request.method == "POST":
        book_id = request.POST.get('bid')
        book = Book.objects.get(id = book_id)
        CopiesAvailable = [x for x in BookCopy.objects.filter(book = book,status = True)]
        if (len(CopiesAvailable) == 0):
            response_data['message'] = "failure"
        else:
            response_data['message'] = "success"
            CopiesAvailable[0].status = False
            CopiesAvailable[0].borrow_date = datetime.today()
            CopiesAvailable[0].borrower = request.user
            CopiesAvailable[0].save()
            
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

    if request.method == "POST":
        BookId = request.POST.get('bookid')
        ReturnedBookCopy = BookCopy.objects.get(id = BookId)
        response_data['message'] = "success"
        ReturnedBookCopy.status = True
        ReturnedBookCopy.borrow_date = None
        ReturnedBookCopy.borrower = None
        ReturnedBookCopy.save()
    
    return JsonResponse(response_data)


@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': None,
    }
    if request.method == "POST":
        response_data['message'] = "success"
        bookId = request.POST.get('bookid')
        rating = request.POST.get('ratingOfTheBook')
        BookWhichIsRated = Book.objects.get(id = bookId) 
        PreviousRatingOfThisUser = RatingOfBook.objects.filter(book = BookWhichIsRated, userWhoRated = request.user)
        if PreviousRatingOfThisUser:
            
            for x in PreviousRatingOfThisUser:
                x.ratingValue = rating
                x.save()

        else:    
            RatingToBeAdded = RatingOfBook()
            RatingToBeAdded.book = BookWhichIsRated
            RatingToBeAdded.ratingValue = rating
            RatingToBeAdded.userWhoRated = request.user
            RatingToBeAdded.save()
        # update rating of the book in the Book model
        Ratings = [x for x in RatingOfBook.objects.filter(book = BookWhichIsRated)]
        l = len(Ratings)
        sum = 0
        for r in Ratings:
            sum = sum + r.ratingValue

        average_rating = sum/l
        BookWhichIsRated.rating = average_rating
        BookWhichIsRated.save()
            
    return JsonResponse(response_data)     

