from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

import urllib.request
import urllib.parse
import json

# Create your views here.
def home(request):
	req = urllib.request.Request('http://models-api:8000/topUsers')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	topUsers = []
	for i in resp:
		topUsers.append(i)
	req2 = urllib.request.Request('http://models-api:8000/recentListings')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	recentListings = []
	for j in resp2:
		recentListings.append(j)
	data = json.dumps([topUsers, recentListings])
	return HttpResponse(data)