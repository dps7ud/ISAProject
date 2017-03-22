from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


import urllib.request
import urllib.parse
import json
import ast
import datetime
import urllib.error
from urllib.error import URLError

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import os
import hmac
from django.conf import settings

# Create your views here.
def home(request):
	if request.method == 'GET':
		errorStrings = ""
		try:
			req = urllib.request.Request('http://models-api:8000/topUsers')
			resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
			try:
				resp = json.loads(resp_json)
			except ValueError:
				resp = False
				errorStrings = resp_json
		except URLError:
			resp = False
			errorStrings = "Timeout Error "
		
		try:
			req2 = urllib.request.Request('http://models-api:8000/recentListings')
			resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
			try:
				resp2 = json.loads(resp_json2)
			except ValueError:
				resp2 = False
				errorStrings = errorStrings + resp_json2
		except URLError as error:
			resp2 = False
			errorStrings = errorStrings + "Timeout Error "
		
		return JsonResponse([resp, resp2, errorStrings], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts GET requests")

def review(request, review_id):
	if request.method == 'GET':
		errorStrings = ""
		try:
			req = urllib.request.Request('http://models-api:8000/api/v1/review/info/' + review_id + '/')
			resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
			try:
				resp = json.loads(resp_json)
			except ValueError:
				resp = False
				errorStrings = resp_json
		except URLError:
			resp = False
			errorStrings = "Timeout Error "
		if resp:
			try:
				req2 = urllib.request.Request('http://models-api:8000/api/v1/user/info/' + str(resp["postee_user"]) + '/')
				resp_json2 = urllib.request.urlopen(req2,timeout=5).read().decode('utf-8')
				try:
					resp2 = json.loads(resp_json2)
				except ValueError:
					resp2 = False
					errorStrings = errorStrings + resp_json2
			except URLError:
				resp2 = False
				errorStrings = errorStrings + "Timeout Error "

			try:
				req3 = urllib.request.Request('http://models-api:8000/api/v1/user/info/' + str(resp["poster_user"]) + '/')
				resp_json3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
				try:
					resp3 = json.loads(resp_json3)
				except ValueError:
					resp3 = False
					errorStrings = errorStrings + resp_json3
			except URLError:
				resp3 = False
				errorStrings = errorStrings + "Timeout Error "

			try:
				req4 = urllib.request.Request('http://models-api:8000/api/v1/task/info/' + str(resp["task"]) + '/')
				resp_json4 = urllib.request.urlopen(req4, timeout=5).read().decode('utf-8')
				try:
					resp4 = json.loads(resp_json4)
				except ValueError:
					resp4 = False
					errorStrings = errorStrings + resp_json4
			except URLError:
				resp4 = False
				errorStrings = errorStrings + "Timeout Error "
		else:
			resp2 = False
			resp3 = False
			resp4 = False

		return JsonResponse([resp, resp2, resp3, resp4, errorStrings], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts GET requests")

def task(request, task_id):
	if request.method == 'GET':
		errorStrings = ""
		try:
			req = urllib.request.Request('http://models-api:8000/api/v1/task/info/' + task_id + '/')
			resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
			try:
				resp = json.loads(resp_json)
			except ValueError:
				resp = False
				errorStrings = resp_json
		except URLError:
			resp = False
			errorStrings = "Timeout Error "
		
		try:
			req2 = urllib.request.Request('http://models-api:8000/api/v1/taskOwners/' + task_id + '/')
			resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
			try:
				resp2 = json.loads(resp_json2)
			except ValueError:
				resp2 = False
				errorStrings = errorStrings + resp_json2
		except URLError:
			resp2 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req3 = urllib.request.Request('http://models-api:8000/api/v1/taskWorkers/' + task_id + '/')
			resp_json3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
			try:
				resp3 = json.loads(resp_json3)
			except ValueError:
				resp3 = False
				errorStrings = errorStrings + resp_json3
		except URLError:
			resp3 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req4 = urllib.request.Request('http://models-api:8000/api/v1/taskSkills/' + task_id + '/')
			resp_json4 = urllib.request.urlopen(req4, timeout=5).read().decode('utf-8')
			try:
				resp4 = json.loads(resp_json4)
			except ValueError:
				resp4 = False
				errorStrings = errorStrings + resp_json4
		except URLError:
			resp4 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req5 = urllib.request.Request('http://models-api:8000/api/v1/taskReviews/' + task_id + '/')
			resp_json5 = urllib.request.urlopen(req5).read().decode('utf-8')
			try:
				resp5 = json.loads(resp_json5)
			except ValueError:
				resp5 = False
				errorStrings = errorStrings + resp_json5
		except URLError:
			resp5 = False
			errorStrings = errorStrings + "Timeout Error "
		return JsonResponse([resp, resp2, resp3, resp4, resp5, errorStrings], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts GET requests")

def user(request, user_id):
	if request.method == 'GET':
		errorStrings = ""
		try:
			req = urllib.request.Request('http://models-api:8000/api/v1/user/info/' + user_id + '/')
			resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
			try:
				resp = json.loads(resp_json)
			except ValueError:
				resp = False
				errorStrings = resp_json
		except URLError:
			resp = False
			errorStrings = "Timeout Error "		
		try:
			req2 = urllib.request.Request('http://models-api:8000/api/v1/userLanguages/' + user_id + '/')
			resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
			try:
				resp2 = json.loads(resp_json2)
			except ValueError:
				resp2 = False
				errorStrings = errorStrings + resp_json2
		except URLError:
			resp2 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req3 = urllib.request.Request('http://models-api:8000/api/v1/userSkills/' + user_id + '/')
			resp_json3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
			try:
				resp3 = json.loads(resp_json3)
			except ValueError:
				resp3 = False
				errorStrings = errorStrings + resp_json3
		except URLError:
			resp3 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req4 = urllib.request.Request('http://models-api:8000/api/v1/userOwnerTasks/' + user_id + '/')
			resp_json4 = urllib.request.urlopen(req4, timeout=5).read().decode('utf-8')
			try:
				resp4 = json.loads(resp_json4)
			except ValueError:
				resp4 = False
				errorStrings = errorStrings + resp_json4
		except URLError:
			resp4 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req5 = urllib.request.Request('http://models-api:8000/api/v1/userWorkerTasks/' + user_id + '/')
			resp_json5 = urllib.request.urlopen(req5, timeout=5).read().decode('utf-8')
			try:
				resp5 = json.loads(resp_json5)
			except ValueError:
				resp5 = False
				errorStrings = errorStrings + resp_json5
		except URLError:
			resp5 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req6 = urllib.request.Request('http://models-api:8000/api/v1/userReviews/' + user_id + '/')
			resp_json6 = urllib.request.urlopen(req6, timeout=5).read().decode('utf-8')
			try:
				resp6 = json.loads(resp_json6)
			except ValueError:
				resp6 = False
				errorStrings = errorStrings + resp_json6
		except URLError:
			resp6 = False
			errorStrings = errorStrings + "Timeout Error "

		try:
			req7 = urllib.request.Request('http://models-api:8000/api/v1/userReviewed/' + user_id + '/')
			resp_json7 = urllib.request.urlopen(req7,timeout=5).read().decode('utf-8')
			try:
				resp7 = json.loads(resp_json7)
			except ValueError:
				resp7 = False
				errorStrings = errorStrings + resp_json7
		except URLError:
			resp7 = False
			errorStrings = errorStrings + "Timeout Error "

		
		return JsonResponse([resp, resp2, resp3, resp4, resp5, resp6, resp7, errorStrings], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts GET requests")

def signup(request):
	if request.method == "POST":
		errorStrings = False
		post_encoded = urllib.parse.urlencode((request.POST).dict()).encode('utf-8')
		logger.error('testing')
		logger.error(str(post_encoded))
		req = urllib.request.Request('http://models-api:8000/api/v1/user/create/', data=post_encoded, method='POST')
		resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
		try:
			resp = json.loads(resp_json)
		except ValueError:
			return JsonResponse([False, False, resp_json], safe=False)
		authenticator = hmac.new(
		        key = settings.SECRET_KEY.encode('utf-8'),
		        msg = os.urandom(32),
		        digestmod = 'sha256',
		    ).hexdigest()
		logger.error(authenticator)
		auth_encoded = urllib.parse.urlencode({"username": resp["username"], "authenticator": authenticator}).encode('utf-8')
		req2 = urllib.request.Request('http://models-api:8000/api/v1/authenticator/create/', data=auth_encoded, method='POST')
		resp2_json = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
		try:
			resp2 = json.loads(resp2_json)
		except ValueError:
			resp2 = False
			errorStrings = resp2_json
		return JsonResponse([resp2, resp, errorStrings], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts POST requests")

def login(request):
	if request.method == "POST":
		errorStrings = ""
		post_encoded = urllib.parse.urlencode((request.POST).dict()).encode('utf-8')
		req = urllib.request.Request('http://models-api:8000/api/v1/user/find/', data=post_encoded, method='POST')
		resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
		if resp == "Correct":
			authenticator = hmac.new(
			        key = settings.SECRET_KEY.encode('utf-8'),
			        msg = os.urandom(32),
			        digestmod = 'sha256',
			    ).hexdigest()
			logger.error(authenticator)
			auth_encoded = urllib.parse.urlencode({"username": request.POST["username"], "authenticator": authenticator}).encode('utf-8')
			req2 = urllib.request.Request('http://models-api:8000/api/v1/authenticator/create/', data=auth_encoded, method='POST')
			resp2_json = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
			try:
				resp2 = json.loads(resp2_json)
			except ValueError:
				resp2 = False
				errorStrings = resp2_json
			return JsonResponse([resp2, errorStrings], safe=False)
		else:
			return JsonResponse([False, resp], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts POST requests")

def logout(request):
	if request.method == "POST":
		post_encoded = urllib.parse.urlencode((request.POST).dict()).encode('utf-8')
		req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/find/' + request.POST["username"] + '/')
		resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
		try: 
			resp = json.loads(resp_json)
		except ValueError:
			return JsonResponse([False, resp], safe=False)
		for i in resp:
			delreq = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' + str(i["authenticator"]) + '/', method="DELETE")
			resp_json = urllib.request.urlopen(delreq, timeout=5).read().decode('utf-8')
		return JsonResponse(["Success", ""], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts POST requests")

def createListing(request):
	if request.method == "POST":
		
		respDict = (request.POST).dict()
		
		auth = respDict["auth"]
		
		req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' + str(auth) + '/', method="GET")
		resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
		
		if resp != "Auth Correct":
			return JsonResponse([False, "ERROR: Invalid Auth"], safe=False)
		
		# listing_dict = listing.dict()
		# logger.error("listing_dict")
		# logger.error(listing_dict)
		del respDict["auth"]
		respDict["status"] = "ACC"
		respDict["time_to_live"] = "2017-02-15"
		respDict["post_date"] = "2017-02-15"
		logger.error(respDict)
		post_encoded = urllib.parse.urlencode(respDict).encode('utf-8')
		req2 = urllib.request.Request('http://models-api:8000/api/v1/task/create/', data=post_encoded, method='POST')
		resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
		try:
			resp2 = json.loads(resp_json2)
		except ValueError:
			logger.error("resp_json2")
			logger.error(resp_json2)
			return JsonResponse([False, resp_json2])
		logger.error("resp2")
		logger.error(resp2)
		return JsonResponse([resp2, False], safe=False)
	else:
		return HttpResponse("ERROR: Endpoint only accepts POST requests")











