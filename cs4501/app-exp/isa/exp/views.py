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

def review(request, review_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/review/' + review_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	req2 = urllib.request.Request('http://models-api:8000/api/v1/user/' + str(resp[0]["fields"]["postee_user"]) + '/')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	req3 = urllib.request.Request('http://models-api:8000/api/v1/user/' + str(resp[0]["fields"]["poster_user"]) + '/')
	resp_json3 = urllib.request.urlopen(req3).read().decode('utf-8')
	resp3 = json.loads(resp_json3)
	req4 = urllib.request.Request('http://models-api:8000/api/v1/task/info/' + str(resp[0]["fields"]["task"]) + '/')
	resp_json4 = urllib.request.urlopen(req4).read().decode('utf-8')
	resp4 = json.loads(resp_json4)
	data = json.dumps([resp, resp2, resp3, resp4])
	return HttpResponse(data)