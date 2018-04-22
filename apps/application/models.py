from django.db import models
import bcrypt
import re


# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData, isNew):
        errors = {}

        #if it's a registration
        if isNew == True:

            #check if any fields are blank
            if len(postData['name']) < 2:
                errors["name_blank"] = "Name must be at least 2 characters."
            if len(postData['alias']) < 2:
                errors["alias_blank"] = "Alias be at least 2 characters."
            if len(postData['email']) < 1:
                errors["email_blank"] = "Email cannot be blank."
            if len(postData['password']) < 1:
                errors["pw_blank"] = "Password cannot be blank."
            if not re.search('\d.*[A-Z]|[A-Z].*\d', postData['password']):
                errors['pw_format'] = "Password must contain at least 1 uppercase letter and 1 number."

            #check if email is valid address
            elif not EMAIL_REGEX.match(postData['email']):
                errors["format_invalid"] = "Please enter a valid email address."


        #check if email already in the database/if is a new user.
            user = User.objects.filter(email = postData['email'])
            if len(user):
                errors['exists'] = "User account already exists."
            if postData["password"] != postData["password2"]:
                errors['mismatch_pw'] = "Passwords must match."

        if isNew == False:
            if not EMAIL_REGEX.match(postData['email']):
                errors["format_invalid"] = "Please enter a valid email address."
            
            user = User.objects.filter(email=postData["email"])
            if len(user) == 0:
                errors["no_user"] = "Log in failed."

            else:
                user = User.objects.get(email=postData['email'])
                encoded_pw = user.password.encode()

                #if email in the database, check if passwords match, decrypting password first.
                if user:
                    print("password = ", postData["password"])

                    if bcrypt.hashpw(postData["password"].encode(), user.password.encode()) != encoded_pw:
                        errors["password_fail"] = "Incorrect password"


        return errors

    def new_review_validator(self, postData):
        errors = {}

        #check if any fields are blank
        if len(postData['title']) < 2:
            errors["title_blank"] = "Title must be at least 2 characters."
        if len(postData['review']) < 10:
            errors["review_blank"] = "Review be at least 10 characters."
        if len(postData['author']) < 2 and len(postData['author_new']) < 2:
            errors["author_blank"] = "Author must not be blank"

        return errors

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.password)

class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __repr__(self):
        return "<Author object: {}>".format(self.name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    reviews = models.ManyToManyField(User, through="Review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __repr__(self):
        return "<Book object: {}>".format(self.title)



class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_reviewed = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __repr__(self):
        return "<Review object: {} {}>".format(self.book_reviewed, self.reviewer)

# class Person(models.Model):
#     name = models.CharField(max_length=128)

#     def __str__(self):
#         return self.name

# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(Person, through='Membership')

#     def __str__(self):
#         return self.name

# class Membership(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     date_joined = models.DateField()
#     invite_reason = models.CharField(max_length=64)
