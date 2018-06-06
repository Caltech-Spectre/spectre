from datetime import datetime, date

from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Book, User, Loan, History
from .forms import LoginForm, SearchForm

#returns a list of books which contain each of the words (substrings separated by spaces) in filterText in either their spectre_id, idcode, isbn, author, or title
def filterBooks(filterText):
    filterList = filterText.split(" ")
    filteredList = Book.objects.all()
    for f in filterList:
        if f != None and f != "":
            filteredList = filteredList.filter(Q(id__icontains=f) | Q(idcode__icontains=f) | Q(isbn__icontains=f) | Q(author__icontains=f) | Q(title__icontains=f))
    return filteredList

#returns a list of users which contain each of the words (substrings separated by spaces) in filterText in either their name or email or cardnum
def filterUsers(filterText):
    filterList = filterText.split(" ")
    return User.objects.filter(Q(name__icontains=str(filterText)) | Q(email__icontains=str(filterText)) | Q(cardnum=filterText))

    for f in filterList:
        if f != None and f != "":
            if f.isdigit():
                f = int(f)
            filteredList = filteredList.filter(Q(name__icontains=str(f)) | Q(email__icontains=str(f)) | Q(cardnum__icontains=f))
    return filteredList

#returns a list of users which contain each of the words (substrings separated by spaces) in filterText in either their name or email
def filterUsersWithoutCardnum(filterText):
    filterList = filterText.split(" ")
    filteredList = User.objects.all()
    for f in filterList:
        if f != None and f != "":
            filteredList = filteredList.filter(Q(name__icontains=f) | Q(email__icontains=f))
    return filteredList

#The main page of Spectre
@csrf_exempt
def mainPage(request):
    context = {}
    return render(request, 'library/mainPageTemplate.html', context)

# @csrf_exempt
def showUser(request):
    userid = request.session.get('userid', None)
    f = request.GET.get('filter', None)
    if f:
        form = SearchForm(request.GET)
    else:
        form = SearchForm(None)
    if userid:
        if f and form.is_valid():
            filter = form.cleaned_data['filter']
            books = Book.objects.filter(Q(id__icontains=filter) | Q(idcode__icontains=filter) | Q(isbn__icontains=filter) | Q(author__icontains=filter) | Q(title__icontains=filter))
        else:
            books = Book.objects.all()
        p = Paginator(books, 25)
        page = int(request.GET.get('page', 1))
        count = len(books)
        start = (page-1)*25 + 1
        end = (page-1)*25+25
        if end > count:
            end = count
        return render(request, 'library/user.html',
                      {'userid': userid, 'username': User.objects.get(id=userid).name,
                       'count': count, 'books':p.get_page(page), 'page':page,
                       'start':start, 'end':end, 'filter':f, 'form':form})
    else:
        return redirect('/login/')

#userpage is just a matter of sending the template with the right things in it.
@csrf_exempt
def userPage(request, spectreUserId):
    user = User.objects.get(id=int(spectreUserId))
    user.lastactive=date.today()
    user.save()
    return render(request, 'library/userPageTemplate.html', {'userid':spectreUserId, 'username':User.objects.get(id=spectreUserId).name, 'books':len(Book.objects.all())})


def logout(request):
    del request.session['userid']
    return redirect('home')

#loginPage is the main database page and the page you have to log in to to reach it.
# @csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            caltech_id = form.cleaned_data['caltech_id']
            users = User.objects.filter(cardnum=caltech_id)
            if users.count() >= 1:
                user = users[0]
                request.session.set_expiry(300)
                request.session['userid'] = user.id
                return redirect('user')
            messages.warning(request, "User not found.")

        else:
            messages.warning(request, 'Please input a Caltech UID.')
    else:
        form = LoginForm()

    return render(request, 'library/login.html', {'form':form})


"""
an addUser request, which will accept a name, email, and cardnum input and add that user to the database, and return the login page, or if those inputs fail, send you the add user page with whatever was input in the input boxes, and a big fat error message to tell you what you did wrong.
"""
@csrf_exempt
def addUser(request):
    this_name = ""
    this_email = ""
    this_cardnum = ""
    try:
        this_name = request.POST['name']
        this_email = request.POST['email']
        this_cardnum = request.POST['cardnum']
        if (this_cardnum == ""):
            this_cardnum = None
        if (this_name == ""):
            return render(request, 'library/addUserTemplate.html', {'error':'FILL IN YOUR NAME', 'name':this_name, 'email':this_email, 'cardnum':this_cardnum})
        if this_cardnum != None:
            try:
                this_cardnum = int(this_cardnum)
            except ValueError:
                return render(request, 'library/addUserTemplate.html', {'error':'DESIGNATION MUST BE A NUMBER', 'name':this_name, 'email':this_email, 'cardnum':this_cardnum})

        users = User.objects.filter(Q(name=this_name)|Q(email=this_email)|(Q(cardnum=this_cardnum)&Q(cardnum__isnull=False)))
        if len(users) > 0:
            return redirect('user')
        user = User(name=this_name, email=this_email, cardnum=this_cardnum, created = date.today(), lastactive = date.today())
        user.save()
        return loginPage(request)
    except KeyError:
        return render(request, 'library/addUserTemplate.html', {'error':'', 'name':this_name, 'email':this_email, 'cardnum':this_cardnum})

def checkout(request):
    userid = request.session.get('userid', None)
    if not userid:
        return redirect('/login/')

    id = request.GET.get('id', None)
    idcode = request.GET.get('idcode', None)
    if id:
        book = get_object_or_404(Book, id=id)
        loan = Loan(lbook=book, luser=User.objects.get(id=userid), date=date.today())
        loan.save()
        book.last = date.today()
        if book.checkouts == None:
            book.checkouts = 0
        book.checkouts = book.checkouts + 1
        book.bloan = loan
        book.save()
        return render(request, 'library/checkedout.html', {'book':book})
    elif idcode:
        return redirect("{}?idcode={}".format(reverse('book'), idcode))
    return render(request, 'library/checkout.html')

def checkin(request):
    userid = request.session.get('userid', None)
    if not userid:
        return redirect('/login/')

    id = request.GET.get('id', None)
    if id:
        book = get_object_or_404(Book, id=id)
        loan = Loan.objects.get(lbook=book.id)
        book.bloan = None
        book.save()
        loan.delete()
    return redirect('user')


def my_books(request):
    userid = request.session.get('userid', None)
    if not userid:
        return redirect('/login/')
    user = User.objects.get(id=userid)
    loans = Loan.objects.filter(luser=user.id)
    print(len(loans))
    return render(request, 'library/my_books.html', {'user':user, 'loans':loans})


def showBook(request):
    userid = request.session.get('userid', None)
    if not userid:
        return redirect('/login/')
    idcode = request.GET.get('idcode', None)
    id = request.GET.get('id', None)
    if idcode:
        books = Book.objects.filter(idcode=idcode)
        if len(books) == 1:
            return render(request, 'library/book.html', {'book':books[0]})
        else:
            print('Count is bigger: {}'.format(len(books)))
    elif id:
        books = Book.objects.filter(id=id)
        if len(books) == 1:
            return render(request, 'library/book.html', {'book':books[0]})
        else:
            print('Count is bigger: {}'.format(len(books)))

#just sends back the number of books a search would return, accepts same stuff as a search
@csrf_exempt
def bookPageSearchCount(request):
    filterText = ""
    try:
        userid = request.GET['userid']
        book_list = []
        for loan in Loan.objects.filter(luser__id=int(userid)):
            book_list.append(loan.lbook)
    except KeyError:
        try:
            filterText = request.POST['filter']
        except KeyError:
            pass
        book_list = filterBooks(filterText)
    return HttpResponse(str(len(book_list)))

"""
takes a min_num, a max_num, a userid, a filter, and an echo, 
Returns an xml list of books that match the filter from the min_num to the max_num (so if 3000 books match the filter, you can get the middle 1000 by setting min_num to 1000 and max_num to 1999).
"""
@csrf_exempt
def bookXMLSearch(request):
    min_num = 0
    max_num = len(Book.objects.all())
    try:
        min_num = request.REQUEST['min_num']
    except KeyError:
        pass
    max_num = len(Book.objects.all())
    try:
        max_num = request.REQUEST['max_num']
    except KeyError:
        pass
    filterText = ""
    try:
        userid = request.REQUEST['userid']
        book_list = []
        for loan in Loan.objects.filter(luser__id=int(userid)):
            book_list.append(loan.lbook)
    except KeyError:
        try:
            filterText = request.REQUEST['filter']
        except KeyError:
            pass
        book_list = filterBooks(filterText)[ min_num:max_num ]
    doc=Document();
    library = doc.createElement("library")
    doc.appendChild(library)
    for book in book_list:
        library.appendChild(book.xml())
    try:
        echoText = request.REQUEST['echo']
        echo = doc.createElement("echo");
        echo.appendChild(doc.createTextNode(escape(echoText)))
        library.appendChild(echo)
    except KeyError:
        pass
    return HttpResponse(doc.toxml(),  mimetype="text/xml")






"""
returns the detailed xml version of a book, provided with a book_id
if given a userid, it will also accept any input value for checkout to check out a book and any for checkin to check in a book.
"""
@csrf_exempt
def bookXML(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        userid = request.GET['userid']
        try:
            check = request.POST['checkout']
            loan = Loan(lbook=book, luser=User.objects.get(id=userid), date = datetime.date.today())
            loan.save()
            book.last=datetime.date.today()
            if book.checkouts==None:
                book.checkouts=0
            book.checkouts = book.checkouts+1
            book.bloan=loan
            book.save()
        except KeyError:
            pass
        try:
            check = request.REQUEST['checkin']
            loan = Loan.objects.get(lbook__id = book_id)
            history = History(luser=User.objects.get(id=userid), lbook=Book.objects.get(id=book_id), dateout=loan.date, datein=datetime.date.today())
            history.save()
            loan.delete()
            book.last=None
            book.bloan=None
            book.save()
        except KeyError:
            pass
    except KeyError:
        pass
    doc=Document();
    doc.appendChild(book.xml(True))
    return HttpResponse(doc.toxml(),  mimetype="text/xml")


