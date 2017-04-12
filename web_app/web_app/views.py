from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import *

import json
import logging
import urllib.parse
import urllib.request

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def four_oh_four(request):
    return HttpResponse("<h2>four-oh-four</h2>")

def home(request):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = "yes"
    else:
        auth = "no"
    successString = success_messaging(request)
    
    req = urllib.request.Request('http://exp-api:8000/home/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp[2] == "":
        errorString = False
    else:
        errorString = resp[2]
    context = {
        'top_users_list': resp[0],
        'recent_listings_list': resp[1],
        'errors': errorString,
        'success': successString,
        'auth': auth
    }
    # return HttpResponse(topUsers)
    return render(request, 'web_app/home.html', context)

def review(request, review_id):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = "yes"
    else:
        auth = "no"
    successString = success_messaging(request)
    req = urllib.request.Request('http://exp-api:8000/review/' + review_id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp[4] == "":
        errorString = False
    else:
        errorString = resp[4]
    context = {
        'review': resp[0],
        'postee': resp[1],
        'poster': resp[2],
        'task': resp[3],
        'errors': errorString,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/review.html', context)
    # return HttpResponse(resp[2][0])

def task(request, task_id):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    if auth:
        auth = "yes"
    else:
        auth = "no"
    logger.error("In task method")
    req = urllib.request.Request('http://exp-api:8000/task/' + task_id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp[5] == "":
        errorString = False
    else:
        errorString = resp[5]
    context = {
        'task': resp[0],
        'owners': resp[2],
        'workers': resp[3],
        'skills': resp[1],
        'reviews': resp[4],
        'errors': errorString,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/task.html', context)

def task_all(request):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    logger.error("task all")
    if auth:
        auth = "yes"
    else:
        auth = "no"  
    req = urllib.request.Request('http://exp-api:8000/' + request.get_full_path())
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    context = {
        'tasks': resp,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/task_all.html', context)

def user_all(request):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    if auth:
        auth = "yes"
    else:
        auth = "no"  
    req = urllib.request.Request('http://exp-api:8000/' + request.get_full_path())
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    context = {
        'users': resp,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/user_all.html', context)

def search(request):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    if auth:
        auth = "yes"
    else:
        auth = "no"
    starter = "reg"
    if "type" in request.GET:
        if request.GET["type"] == "user":
            starter = "user"
        if request.GET["type"] == "review":
            starter = "review"

    req = urllib.request.Request('http://exp-api:8000/' + request.get_full_path())
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    context = {
        'tasks': resp[0],
        'users': resp[1],
        'reviews': resp[2],
        'start': starter,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/search.html', context)


def review_all(request):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    if auth:
        auth = "yes"
    else:
        auth = "no"  
    req = urllib.request.Request('http://exp-api:8000/' + request.get_full_path())
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    context = {
        'reviews': resp,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/review_all.html', context)

def user(request, user_id):
    auth = request.COOKIES.get('auth')
    successString = success_messaging(request)
    if auth:
        auth = "yes"
    else:
        auth = "no"
    logger.error("In user method")
    req = urllib.request.Request('http://exp-api:8000/user/' + user_id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    logger.error(resp)
    if resp[7] == "":
        errorString = False
    else:
        errorString = resp[7]

    context = {
        'user': resp[0],
        'languages': resp[1],
        'skills': resp[2],
        'owner': resp[3],
        'worker': resp[4],
        'reviewer': resp[5],
        'reviewee': resp[6],
        'errors': errorString,
        'auth': auth,
        'success': successString
    }
    return render(request, 'web_app/user.html', context)

def signup(request):
    auth = request.COOKIES.get('auth')
    if auth:
        auth = "yes"
    else:
        auth = "no"
    successString = success_messaging(request)
    errors = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            userInfo = form.cleaned_data
            userInfo["user_skills"] = request.POST["user_skills"]
            userInfo["spoken_languages"] = request.POST["spoken_languages"]
            post_encoded = urllib.parse.urlencode(userInfo).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/signup/', 
                    data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if resp[2]:
                errors = resp[2]
            else:
                response = HttpResponseRedirect(reverse('user', args=[resp[1]["id"]])
                        + "?success=signup")
                response.set_cookie("auth", resp[0]["authenticator"])
                return response         
        else:
            # Better to allow some data missing and indicate required fields.
            errors = "Missing data"
    else:
        form = SignUpForm()
    
    return render(request, 'web_app/signup.html', {'form': form, 'errors': errors, 'auth': auth, 'success': successString})

def login(request):
    errors = False
    try:
        nextStop = request.GET["next"]
    except:
        nextStop = False
    successString = success_messaging(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            post_encoded = urllib.parse.urlencode(form.cleaned_data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/login/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp[0]:
                errors = resp[1]
            else:
                if nextStop:
                    response = HttpResponseRedirect(nextStop + "?success=login")
                else:
                    response = HttpResponseRedirect(reverse('home') + "?success=login")
                response.set_cookie("auth", resp[0]["authenticator"])
                return response
    else:
        form = LoginForm()

    return render(request, 'web_app/login.html', 
            {
                'form': form, 
                'errors': errors, 
                'next': nextStop, 
                'success': successString
            })

def logout(request):
    auth = request.COOKIES.get('auth')
    #   Make request to the experience layer '/logout'
    # Delete all of the auth cookies
    post_encoded = urllib.parse.urlencode({"authenticator": auth}).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/logout/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = HttpResponseRedirect(reverse('home') + "?success=logout")
    response.delete_cookie("auth")
    return response

def create_listing(request):
    successString = success_messaging(request)
    auth = request.COOKIES.get('auth')
    
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))

    errors = False
    authString = "yes"

    if request.method == 'POST':
        logger.error("in post of web app create listing")
        form = CreateListingForm(request.POST)
        if form.is_valid():
            logger.error("Form is valid")
            listingInfo = form.cleaned_data
            listingInfo["auth"] = auth;
            listingInfo["skills"] = request.POST["required_skills"]
            post_encoded = urllib.parse.urlencode(listingInfo).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/createListing/', 
                    data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp[0]:
                logger.error(resp[1])
                errors = resp[1]
                if resp[1] == "ERROR: Invalid Auth":
                    return HttpResponseRedirect(reverse("login") + "?next=" 
                            + reverse("create_listing"))
            else:
                response = HttpResponseRedirect(reverse('task', args=[resp[0]['id']]) 
                        + "?success=createListing")
                return response
        else:
            errors = form.errors
    else:
        form = CreateListingForm()

    return render(request, 'web_app/createlisting.html', 
            {
                'form': form,
                'auth':  authString,
                'errors': errors, 
                'success': successString
            })

def profile(request):
    successString = success_messaging(request)
    auth = request.COOKIES.get('auth')
    
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("profile"))

    authString = "yes"

    req = urllib.request.Request('http://exp-api:8000/profile/' + auth + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    logger.error(resp)
    if not resp[2]:
        errorString = resp[2]
    else:
        errorString = False

    context = {
        'userID': resp[1],
        'neededReviews': resp[0],
        'auth':  authString,
        'errors': errorString, 
        'success': successString
    }
    return render(request, 'web_app/profile.html', context)

def create_review(request):
    
    auth = request.COOKIES.get('auth')
    
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("profile"))

    if request.method == "POST":
        logger.error("In createReview")
        respDict = (request.POST).dict()
        respDict["auth"] = auth
        logger.error(respDict)
        post_encoded = urllib.parse.urlencode(respDict).encode('utf-8')
        req = urllib.request.Request('http://exp-api:8000/createReview/', 
                data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        logger.error(resp_json)
        respArray = json.loads(resp_json)
        if not respArray[0]:
            return HttpResponse(respArray[1])
        else:
            return HttpResponse("Success")
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")
    

def success_messaging(request):
    try:
        if request.GET["success"] == "logout":
            return "Successfully Logged Out"
        elif request.GET["success"] == "login":
            return "Successfully Logged In"
        elif request.GET["success"] == "signup":
            return "Successfully Signed Up"
        elif request.GET["success"] == "createListing":
            return "Successfully Created Task"
        else:
            return "Operation Successful"
    except:
        return False

