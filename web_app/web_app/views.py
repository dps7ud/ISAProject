from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from .forms import SignUpForm, LoginForm

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
		'owners': resp[1],
		'workers': resp[2],
		'skills': resp[3],
		'reviews': resp[4],
		'errors': errorString
	}
	return render(request, 'web_app/task.html', context)

def user(request, user_id):
	logger.error("In user method")
	req = urllib.request.Request('http://exp-api:8000/user/' + user_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
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
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			post_encoded = urllib.parse.urlencode(form.cleaned_data).encode('utf-8')
			req = urllib.request.Request('http://exp-api:8000/signup/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			if not resp[1] == "":
				return HttpResponse(resp[1])
			else:
				return HttpResponseRedirect('/user/' + str(resp[0]['id']) + '/')		
	else:
		form = SignUpForm()
	
	return render(request, 'web_app/signup.html', {'form': form})

def login(request):
	errors = False
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
				response = HttpResponseRedirect(reverse('home'))
				response.set_cookie("auth", resp[0]["authenticator"])
				return response
	else:
		form = LoginForm()

	return render(request, 'web_app/login.html', {'form': form, 'errors': errors})



