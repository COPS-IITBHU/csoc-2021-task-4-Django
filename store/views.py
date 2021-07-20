from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book=get_object_or_404(Book, id=bid)
    count=BookCopy.objects.filter(book=book,status=True).count(),
    context = {
        'book':book, 
        'num_available':count, 
    }
    return render(request, template_name, context=context)

@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,
    }
    get_data = request.GET
    if get_data:
        context['books'] = Book.objects.filter(title=get_data['title'], author=get_data['author'], genre=get_data['genre'])
        if len(context['books'])==0:
            messages.error(request, "Book Not Found, See all available books")
            context['books'] = Book.objects.all()
        else:
            messages.success(request, "Book Found")
    else:
        context['books'] = Book.objects.all()
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    books = BookCopy.objects.filter(borrower=request.user)
    context['books'] = books
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    if request.method=="POST":
        book_id=request.POST['bid']
        book=get_object_or_404(Book, id=book_id)
        book=BookCopy.objects.filter(book=book,status=True)
        if len(book)==0:
            messages.error(request, "Book not available")
            return JsonResponse(response_data)
        else:
            book=book[0]
            book.borrower = request.user
            book.borrow_date = timezone.datetime.today().date()
            book.status=False
            book.save()
            response_data['message'] = "success"
            return JsonResponse(response_data)
    else:
        return JsonResponse(response_data)

@csrf_exempt
@login_required
def handelrating(request):
    response_data = {
        'message': None,
    }
    if request.method=="POST":
        book_id=request.POST['bid']
        rating=request.POST['rating']
        bookcopy=BookCopy.objects.filter(id=book_id)
        if len(bookcopy)!=0:
            bookcopy[0].borrower=None
            bookcopy[0].borrow_date =None
            bookcopy[0].status=True
            bookcopy[0].save()
            book=bookcopy[0].book
        ratedbook=BookRating.objects.filter(book=book,ratedUser=request.user)
        if len(ratedbook)==0:
            bookrating=BookRating.objects.create(book=book, rating=rating, ratedUser=request.user)
            bookrating.save()
        else:
            ratedbook=ratedbook[0]
            ratedbook.rating=rating
            ratedbook.save()
        response_data['message'] = "success"
        messages.success(request, "Book successfully return")
        return JsonResponse(response_data)
       
@csrf_exempt
@login_required
def returnBookView(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    tbook=Book.objects.all()
    if len(tbook)!=0:
        for i in tbook:
            ibook=BookRating.objects.filter(book=i)
            if len(ibook)!=0:
                a=0
                for j in ibook:
                    a=a+j.rating
                i.rating=a/len(ibook)
                i.save()
    books = BookCopy.objects.filter(borrower=request.user)
    context['books'] = books
    return render(request, template_name, context=context)

# For SignUp
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return render(request, 'store/index.html')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return render(request, 'store/index.html')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return render(request, 'store/index.html')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iLibrary card has been successfully created")
        return render(request, 'store/index.html')

    else:
        messages.error(request, "Something went wrong! Please try again")
        return render(request, 'store/index.html')

# For Login
def handeLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return render(request, 'store/index.html')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return render(request, 'store/index.html')
    return HttpResponse("404- Not found")

# For Logout
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request, 'store/index.html')  