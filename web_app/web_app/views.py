from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

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
	topUsers = []
	for i in resp[0]:
		topUsers.append(i)
	latestListings = []
	for j in resp[1]:
		latestListings.append(j)
	context = {
		'top_users_list': resp[0],
		'recent_listings_list': resp[1]
	}
	# return HttpResponse(topUsers)
	return render(request, 'web_app/home.html', context)

def review(request, review_id):
	logger.error("In review method")
	req = urllib.request.Request('http://exp-api:8000/review/' + review_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	logger.error(resp)
	context = {
		'review': resp[0],
		'postee': resp[1],
		'poster': resp[2],
		'task': resp[3]
	}
	return render(request, 'web_app/review.html', context)
	# return HttpResponse(resp[2][0])

def task(request, task_id):
	logger.error("In task method")
	req = urllib.request.Request('http://exp-api:8000/task/' + task_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	context = {
		'task': resp[0],
		'owners': resp[1],
		'workers': resp[2],
		'skills': resp[3],
		'reviews': resp[4]
	}
	return render(request, 'web_app/task.html', context)

def user(request, user_id):
	logger.error("In user method")
	req = urllib.request.Request('http://exp-api:8000/user/' + user_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	context = {
		'user': resp[0],
		'languages': resp[1],
		'skills': resp[2],
		'owner': resp[3],
		'worker': resp[4],
		'reviewer': resp[5],
		'reviewee': resp[6]
	}
	return render(request, 'web_app/user.html', context)
