from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


import urllib.request
import urllib.parse
import json

# Create your views here.
def home(request):
	req = urllib.request.Request('http://models-api:8000/topUsers')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	
	req2 = urllib.request.Request('http://models-api:8000/recentListings')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	
	return JsonResponse([resp, resp2], safe=False)

def review(request, review_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/review/' + review_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	req2 = urllib.request.Request('http://models-api:8000/api/v1/user/' + str(resp["postee_user"]) + '/')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	req3 = urllib.request.Request('http://models-api:8000/api/v1/user/' + str(resp["poster_user"]) + '/')
	resp_json3 = urllib.request.urlopen(req3).read().decode('utf-8')
	resp3 = json.loads(resp_json3)
	req4 = urllib.request.Request('http://models-api:8000/api/v1/task/info/' + str(resp["task"]) + '/')
	resp_json4 = urllib.request.urlopen(req4).read().decode('utf-8')
	resp4 = json.loads(resp_json4)
	return JsonResponse([resp, resp2, resp3, resp4], safe=False)

def task(request, task_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/task/info/' + task_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	req2 = urllib.request.Request('http://models-api:8000/api/v1/taskOwners/' + task_id + '/')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	req3 = urllib.request.Request('http://models-api:8000/api/v1/taskWorkers/' + task_id + '/')
	resp_json3 = urllib.request.urlopen(req3).read().decode('utf-8')
	resp3 = json.loads(resp_json3)
	req4 = urllib.request.Request('http://models-api:8000/api/v1/taskSkills/' + task_id + '/')
	resp_json4 = urllib.request.urlopen(req4).read().decode('utf-8')
	resp4 = json.loads(resp_json4)
	req5 = urllib.request.Request('http://models-api:8000/api/v1/taskReviews/' + task_id + '/')
	resp_json5 = urllib.request.urlopen(req5).read().decode('utf-8')
	resp5 = json.loads(resp_json5)
	return JsonResponse([resp, resp2, resp3, resp4, resp5], safe=False)

def user(request, user_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/user/' + user_id + '/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	req2 = urllib.request.Request('http://models-api:8000/api/v1/userLanguages/' + user_id + '/')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	req3 = urllib.request.Request('http://models-api:8000/api/v1/userSkills/' + user_id + '/')
	resp_json3 = urllib.request.urlopen(req3).read().decode('utf-8')
	resp3 = json.loads(resp_json3)
	req4 = urllib.request.Request('http://models-api:8000/api/v1/userOwnerTasks/' + user_id + '/')
	resp_json4 = urllib.request.urlopen(req4).read().decode('utf-8')
	resp4 = json.loads(resp_json4)
	req5 = urllib.request.Request('http://models-api:8000/api/v1/userWorkerTasks/' + user_id + '/')
	resp_json5 = urllib.request.urlopen(req5).read().decode('utf-8')
	resp5 = json.loads(resp_json5)
	req6 = urllib.request.Request('http://models-api:8000/api/v1/userReviews/' + user_id + '/')
	resp_json6 = urllib.request.urlopen(req6).read().decode('utf-8')
	resp6 = json.loads(resp_json6)
	req7 = urllib.request.Request('http://models-api:8000/api/v1/userReviewed/' + user_id + '/')
	resp_json7 = urllib.request.urlopen(req7).read().decode('utf-8')
	resp7 = json.loads(resp_json7)
	return JsonResponse([resp, resp2, resp3, resp4, resp5, resp6, resp7], safe=False)
