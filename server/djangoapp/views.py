# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate
from .models import CarMake, CarModel
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)
# ...

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed


def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


def get_dealers(request):
    try:
        # Chiamata all'API per recuperare i concessionari
        dealers = get_request("/fetchDealers")   
        # Verifica se la risposta è corretta
        if 'status' in dealers and dealers['status'] == 200:
            return JsonResponse({"status": 200, "dealers": dealers})
        else:
            return JsonResponse({"status": 400, "message": "Unable to fetch dealers"})
    except Exception as e:
        logger.error(f"Error fetching dealers: {e}")
        return JsonResponse({"status": 500, "message": "Internal Server Error"})
    

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
    


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
    

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
    
    
    
    # Create a `get_cars` view to render a list of all cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(f"Numero di CarMake presenti: {count}")
    if count == 0:
        print("Popolamento del database in corso...")
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})