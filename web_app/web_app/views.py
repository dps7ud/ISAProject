from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from .forms import SignUpForm, LoginForm, CreateListingForm

import urllib.request
import urllib.parse
import json

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def four_oh_four(request):
    return HttpResponse("<h2>four-oh-four</h2>")

def home(request):
	logger.error("In home method")
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
		'errors': errorString
	}
	# return HttpResponse(topUsers)
	return render(request, 'web_app/home.html', context)

def review(request, review_id):
	logger.error("In review method")
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
		'errors': errorString
	}
	return render(request, 'web_app/review.html', context)
	# return HttpResponse(resp[2][0])

def task(request, task_id):
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
		'errors': errorString
	}
	return render(request, 'web_app/task.html', context)

def user(request, user_id):
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
		'errors': errorString
	}
	return render(request, 'web_app/user.html', context)

def signup(request):
	errors = False
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			userInfo = form.cleaned_data
			userInfo["user_skills"] = request.POST["user_skills"]
			userInfo["spoken_languages"] = request.POST["spoken_languages"]
			post_encoded = urllib.parse.urlencode(userInfo).encode('utf-8')
			req = urllib.request.Request('http://exp-api:8000/signup/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			if resp[2]:
				errors = resp[2]
			else:
				response = HttpResponseRedirect(reverse('user', args=[resp[1]["id"]]))
				response.set_cookie("auth", resp[0]["authenticator"])
				return response			
	else:
		form = SignUpForm()
	
	return render(request, 'web_app/signup.html', {'form': form, 'errors': errors})

def login(request):
	errors = False
	try:
		nextStop = request.GET["next"]
	except:
		nextStop = False
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
					response = HttpResponseRedirect(nextStop)
				else:
					response = HttpResponseRedirect(reverse('home'))
				response.set_cookie("auth", resp[0]["authenticator"])
				return response
	else:
		form = LoginForm()

	return render(request, 'web_app/login.html', {'form': form, 'errors': errors, 'next': nextStop})

def logout(request):
	#Make request to the experience layer '/logout'
	#Delete all of the auth cookies
	return HttpResponse("Logout")

def create_listing(request):
	auth = request.COOKIES.get('auth')
	
	if not auth:
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))

	errors = False
	if request.method == 'POST':
		logger.error("in post of web app create listing")
		form = CreateListingForm(request.POST)
		if form.is_valid():
			logger.error("Form is valid")
			listingInfo = form.cleaned_data
			listingInfo["auth"] = auth;
			listingInfo["skills"] = request.POST["required_skills"]
			post_encoded = urllib.parse.urlencode(listingInfo).encode('utf-8')
			req = urllib.request.Request('http://exp-api:8000/createListing/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			if not resp[0]:
				logger.error(resp[1])
				errors = resp[1]
				if resp[1] == "ERROR: Invalid Auth":
					return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
			else:
				response = HttpResponseRedirect(reverse('task', args=[resp[0]['id']]))
				return response
		else:
			errors = form.errors
	else:
		form = CreateListingForm()

	return render(request, 'web_app/createlisting.html', {'form': form, 'errors': errors})



