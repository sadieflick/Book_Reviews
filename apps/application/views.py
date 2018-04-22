from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):

    return render(request, "application/index.html")

def books(request):

    if "id" not in request.session:
        messages.error(request, "You must be logged in to enter site.")
        return redirect('/')

    context = {
        "reviews" : Review.objects.all().order_by('created_at')[:3],
        "books" : Book.objects.all(),
        "alias": User.objects.get(id = request.session["id"]).alias
    }
    

    return render(request, "application/books.html", context)

def book_page(request, book_id):

    if "id" not in request.session:
        messages.error(request, "You must be logged in to enter site.")
        return redirect('/')

    context = {
        "book" : Book.objects.get(id=book_id),
        "reviews": Review.objects.filter(book_reviewed = Book.objects.get(id=book_id))
    }
    

    return render(request, "application/book_page.html", context)

def add_page(request):

    if "id" not in request.session:
        messages.error(request, "You must be logged in to enter site.")
        return redirect('/')

    context = {
        "authors" : Author.objects.all()
    }

    return render(request, "application/add_page.html", context)

def user_page(request, user_id):

    if "id" not in request.session:
        messages.error(request, "You must be logged in to enter site.")
        return redirect('/')

    user = User.objects.get(id=user_id)

    context = {
        "user" : user,
        "reviews" : Review.objects.filter(reviewer = user)
    }

    return render(request, "application/user_page.html", context)

def post_review(request):

    book = Book.objects.get(id = request.POST["book_id"])
    reviewer = User.objects.get(id = request.session["id"])
    Review.objects.create(reviewer = reviewer, book_reviewed = book, rating = request.POST["rating"], content = request.POST["content"])


    #do something in database
    return redirect('/books/'+ str(request.POST["book_id"]))

def post_review_new(request):

    print("author post data: ", request.POST["author"])

    errors = User.objects.new_review_validator(request.POST)

    if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/books/add_page')

    reviewer = User.objects.get(id = request.session["id"])

    if Book.objects.filter(title = request.POST["title"]):
        book = Book.objects.get(title = request.POST["title"])
        book_id = book.id
        author = book.author
        Review.objects.create(reviewer = reviewer, book_reviewed = book, rating = request.POST["rating"], content = request.POST["review"])
        return redirect('/books/'+ str(book_id))
    
    else:

        author = None

        if Author.objects.filter(name = request.POST["author"]):
            author = Author.objects.get(name = request.POST["author"])

        else:
            author = Author.objects.create(name = request.POST["author_new"])
            author.save()

        book = Book.objects.create(title = request.POST["title"], author = author)
        book.save()
        book_id = book.id

        Review.objects.create(reviewer = reviewer, book_reviewed = book, rating = request.POST["rating"], content = request.POST["review"])
        
        return redirect('/books/'+ str(book_id))


def submit(request):
    if request.method == "POST":

        print(request.POST)
        print (id)

        #save post info so the user doesn't have to re-type it if they have an error
        request.session["name"] = request.POST["name"]
        request.session["alias"] = request.POST["alias"]
        request.session["email"] = request.POST["email"]

        #get validation manager
        errors = User.objects.basic_validator(request.POST, True)
        #if there are any errors
        if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')

        #use bcrypt to hash password
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        # update from form first_name, last_name, email in db, save id in a variable
        #create user
        new_user = User.objects.create(email =request.POST["email"], name =request.POST["name"], alias =request.POST["alias"], password=hash1)
        new_user.save()

        messages.success(request, "Successfully registered!")
        user = User.objects.get(email=request.POST["email"])
        request.session["id"] = user.id

        return redirect('/books')

def login(request):

    if request.method == "POST":
        
        errors = User.objects.basic_validator(request.POST, False)
        #if there are any errors
        if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request,value)
            # redirect the user back to the form to fix the errors
            return redirect('/')

        else:
            user = User.objects.get(email = request.POST["email"])
            request.session["id"] = user.id
            return redirect('/books')
        

        return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')
    
