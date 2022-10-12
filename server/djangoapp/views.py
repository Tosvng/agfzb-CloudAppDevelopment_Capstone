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

from .models import CarModel

from .restapis import get_dealer_by_id, get_dealer_reviews_from_cf, get_dealers_from_cf, post_request

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
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/Tosvng_Tosvng-space/dealership-package/dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
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
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/Tosvng_Tosvng-space/dealership-package/reviews.json"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context = {
            "reviews":  reviews, 
            "dealer_id": dealer_id
        }

        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    
    if request.user.is_authenticated:
         # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = f"https://us-south.functions.appdomain.cloud/api/v1/web/Tosvng_Tosvng-space/dealership-package/dealership.json?dealerId={dealer_id}"
            # Get dealer details from the API
            print(CarModel.objects.all())
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id)[0],
            }
            return render(request, 'djangoapp/add_review.html', context)
        if request.method == 'POST':
            form = request.POST
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
             # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            json_payload =dict()
            json_payload["review"] = review

             # Performing a POST request with the review
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/Tosvng_Tosvng-space/dealership-package/post-review"  # API Cloud Function route
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        # If user isn't logged in, redirect to login page
        print("User must be authenticated before posting a review. Please log in.")
        return redirect("/djangoapp/login")
