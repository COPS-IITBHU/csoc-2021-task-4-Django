import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


# Create your views here.
def index(request):
    return render(request, 'store/index.html')


def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None,  # set this to an instance of the required book
        'num_available': None,
        # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    try:
        context['book'] = Book.objects.get(pk=bid)
        context['num_available'] = Book.objects.get(pk=bid).number
    except Book.DoesNotExist:
        context['num_available'] = 0

    # START YOUR CODE HERE

    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,  # set this to the list of required books upon filtering using the GET parameters
        # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    q = Book.objects.all()
    if 'title' in get_data:
        if len(get_data['title']) != 0:
            q = q.filter(title=get_data['title'])
    if 'author' in get_data:
        if len(get_data['author']) != 0:
            q = q.filter(author=get_data['author'])
    if 'genre' in get_data:
        if len(get_data['genre']) != 0:
            q = q.filter(genre=get_data['genre'])

    # START YOUR CODE HERE
    context['books'] = q
    return render(request, template_name, context=context)


@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    username = request.user.username
    q = BookCopy.objects.all()
    v = []
    for i in q:
        if str(i.borrower) == str(username):
            v.append(i)
    context['books'] = v
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE

    return render(request, template_name, context=context)


@csrf_exempt
@login_required
def loanBookView(request):
    bid = request.POST['bid']
    response_data = {
        'message': None,
    }
    q = Book.objects.get(pk=bid)

    username = request.user.username
    r = BookCopy.objects.all()
    v = []
    for i in r:
        if str(i.borrower) == str(username):
            v.append(i)
    for i in v:
        if q == i.book:
            response_data['message'] = 'failure'
            break
    else:
        if q.number > 0:
            response_data['message'] = 'success'
            q.number -= 1
            q.save()
            s = BookCopy(book=q, borrower=request.user)
            s.save()
        else:
            response_data['message'] = 'failure'

    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    # get the book id from post data

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
    Data = json.loads(request.body.decode('UTF-8'))
    bid = Data['detail']
    q = Book.objects.get(pk=bid)
    username = request.user.username

    r = BookCopy.objects.all()
    for i in r:
        if str(i.borrower) == str(username) and i.book == q:
            i.delete()
            q.number += 1
            q.save()
            break
    response_data = {
        'message': 'Successful',
    }
    return JsonResponse(response_data)


@csrf_exempt
@login_required
def rateBook(request):
    Data = request.POST
    response_data = {
        'message': 'success',
    }
    rate = Data['rate']
    q = Book.objects.get(pk=Data['bid'])
    username = request.user.username
    r = BookRating.objects.all()
    r = r.filter(book=q)
    for i in r:
        if i.ratedBy == str(username):
            i.rating = rate
            i.save()
            break
    else:
        x = BookRating(book=q, ratedBy=str(username), rating=rate)
        x.save()
    a = 0
    b = 0
    r = BookRating.objects.all()
    r = r.filter(book=q)
    for i in r:
        a += 1
        b += i.rating
    r = b / a
    q.rating = r
    q.save()
    return JsonResponse(response_data)