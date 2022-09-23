from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# = `login_request` view to handle sign in request
def login_request(request):
    context={}
    #Handles POST request
    if request.method == 'POST':
        #Get the username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['pwd']
        #check if the user can be authenticated
        user = authenticate(username = username, password = password)
        
        if user is not None:
            #If user is valid, call login method to login current user
            print(user)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            #if not, return to login page again
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request,'djangoapp/index.html', context)

#`logout_request` view to handle sign out request
def logout_request(request):
    #Get the user object based on the session id in the request
    print("Log out the user`{}`".format(request.user.username))
    #logout user in the request
    logout(request)
    #Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context ={}
    #if it is a get request just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    #If it is a POST request
    elif request.method =='POST':
        #Get user information from request.POST
        username =request.POST['username']
        first_name =request.POST['firstname']
        last_name =request.POST['lastname']
        password =request.POST['psw']
        user_exist =False
        try:
            #check if user already exists 
            User.objects.get(username = username)
            user_exist =True
        except:
            #If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        if not user_exist:
            #create user in auth_user table
            user =User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password)
            #login the user
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

