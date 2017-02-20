from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

import urllib.request
import urllib.parse
import json


# Create your views here.
def home(request):
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
		'top_users_list': topUsers,
		'recent_listings_list': latestListings
	}
	# return HttpResponse(topUsers)
	return render(request, 'web/home.html', context)

