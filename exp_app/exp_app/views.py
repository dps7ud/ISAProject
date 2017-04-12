from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone


from urllib.error import URLError
import datetime
import hmac
import json
from kafka import KafkaProducer
import logging
import os
import urllib.parse
import urllib.request

# Get an instance of a logger
logger = logging.getLogger(__name__)

#Elastic Search Query Creators
def esQueryCreator(request):
    if 'type' not in request.GET:
        return False

    queryObj = {
        "query": {
            "bool": {
                "should": [
                ]
            }
        }
    }
    queryES = False
    allq = False
    title = False
    description = False
    location = False
    status = False
    username = False
    name = False
    email = False
    bio = False
    location = False
    title = False
    body = False
    score = False

    if 'all' in request.GET:
        allq = request.GET['all']
        queryES = True
    if 'title' in request.GET:
        title = request.GET['title']
        queryES = True
    if 'location' in request.GET:
        location = request.GET['location']
        queryES = True
    if 'status' in request.GET:
        status = request.GET['status']
        queryES = True
    if 'description' in request.GET:
        description = request.GET['location']
        queryES = True
    if 'username' in request.GET:
        username = request.GET['username']
        queryES = True
    if 'name' in request.GET:
        name = request.GET['name']
        queryES = True
    if 'email' in request.GET:
        email = request.GET['email']
        queryES = True
    if 'bio' in request.GET:
        bio = request.GET['bio']
        queryES = True
    if 'body' in request.GET:
        body = request.GET['body']
        queryES = True
    if 'score' in request.GET:
        title = request.GET['score']
        queryES = True

    if queryES:
        if allq:
            queryObj['query']['bool']['should'].append({"match": {"_all": allq}})
        if title:
            queryObj['query']['bool']['should'].append({"match": {"title": title}})
        if description:
            queryObj['query']['bool']['should'].append({"match": {"description": description}})
        if location:
            queryObj['query']['bool']['should'].append({"match": {"location": location}})
        if status:
            queryObj['query']['bool']['should'].append({"match": {"title": status}})
        if username:
            queryObj['query']['bool']['should'].append({"match": {"username": username}})
        if name:
            queryObj['query']['bool']['should'].append({"match": {"fname": name}})
            queryObj['query']['bool']['should'].append({"match": {"lname": name}})
        if email:
            queryObj['query']['bool']['should'].append({"match": {"email": email}})
        if bio:
            queryObj['query']['bool']['should'].append({"match": {"bio": bio}})
        if body:
            queryObj['query']['bool']['should'].append({"match": {"body": body}})
        if score:
            queryObj['query']['bool']['should'].append({"match": {"score": float(score)}})
        return queryObj
    else:
        return False

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

def task(request, task_id):
    if request.method == 'GET':
        errorStrings = ""
        try:
            req = urllib.request.Request('http://models-api:8000/api/v1/task/main/' 
                    + task_id + '/')
            resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            resp = json.loads(resp_json)
            return JsonResponse(resp, safe=False)
        except URLError:
            return HttpResponse("Timeout")
        
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def task_all(request):
    if request.method == 'GET':
        esQuery = esQueryCreator(request)
        if esQuery: 
            reqES = urllib.request.Request('http://es:9200/tasktic/' + request.GET['type'] 
                    + '/_search?pretty', data=json.dumps(esQuery).encode('utf-8'), method='POST')
            reqES.add_header('Content-Type', 'application/json')
            respES_json = urllib.request.urlopen(reqES, timeout=5).read().decode('utf-8')
            esResponse = json.loads(respES_json)
            hitArray = esResponse["hits"]["hits"]
            finalArray = []
            for i in hitArray:
                iDict = i["_source"]
                finalArray.append(iDict)
            return JsonResponse(finalArray, safe=False)
        else:
            errorStrings = ""
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/task/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                return JsonResponse(resp, safe=False)
            except URLError:
                return HttpResponse("Timeout")
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def user_all(request):
    if request.method == 'GET':
        esQuery = esQueryCreator(request)

        if esQuery: 
            reqES = urllib.request.Request('http://es:9200/tasktic/' + request.GET['type'] 
                    + '/_search?pretty', data=json.dumps(esQuery).encode('utf-8'), method='POST')
            reqES.add_header('Content-Type', 'application/json')
            respES_json = urllib.request.urlopen(reqES, timeout=5).read().decode('utf-8')
            logger.error("respES_json: " + str(respES_json)) 
            esResponse = json.loads(respES_json)
            hitArray = esResponse["hits"]["hits"]
            finalArray = []
            for i in hitArray:
                iDict = i["_source"]
                finalArray.append(iDict)
            return JsonResponse(finalArray, safe=False)
        else:
            logger.error("")
            errorStrings = ""
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/user/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                logger.error(resp)
                return JsonResponse(resp, safe=False)
            except URLError:
                return HttpResponse("Timeout")
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def review_all(request):
    if request.method == 'GET':
        esQuery = esQueryCreator(request)

        if esQuery: 
            reqES = urllib.request.Request('http://es:9200/tasktic/' + request.GET['type'] 
                    + '/_search?pretty', data=json.dumps(esQuery).encode('utf-8'), method='POST')
            reqES.add_header('Content-Type', 'application/json')
            respES_json = urllib.request.urlopen(reqES, timeout=5).read().decode('utf-8')
            logger.error("respES_json: " + str(respES_json)) 
            esResponse = json.loads(respES_json)
            hitArray = esResponse["hits"]["hits"]
            finalArray = []
            for i in hitArray:
                iDict = i["_source"]
                finalArray.append(iDict)
            return JsonResponse(finalArray, safe=False)
        else:
            logger.error("")
            errorStrings = ""
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/review/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                logger.error(resp)
                return JsonResponse(resp, safe=False)
            except URLError:
                return HttpResponse("Timeout")
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def search(request):
    if request.method == 'GET':
        esQuery = esQueryCreator(request)
        tasks = False
        users = False
        reviews = False
        if esQuery:
            if request.GET['type'] == 'all':
                reqES = urllib.request.Request('http://es:9200/tasktic/_search?pretty', data=json.dumps(esQuery).encode('utf-8'), method='POST')
                reqES.add_header('Content-Type', 'application/json')
                respES_json = urllib.request.urlopen(reqES, timeout=5).read().decode('utf-8')
                logger.error("respES_json: " + str(respES_json)) 
                esResponse = json.loads(respES_json)
                hitArray = esResponse["hits"]["hits"]
                tasks = []
                users = []
                reviews = []
                for i in hitArray:
                    iDict = i["_source"]
                    if i["_type"] == "task":
                        tasks.append(iDict)
                    if i["_type"] == "user":
                        users.append(iDict)
                    if i["_type"] == "review":
                        reviews.append(iDict)
                return JsonResponse([tasks, users, reviews], safe=False)
            else:
                reqES = urllib.request.Request('http://es:9200/tasktic/' + request.GET['type'] + '/_search?pretty', data=json.dumps(esQuery).encode('utf-8'), method='POST')
                reqES.add_header('Content-Type', 'application/json')
                respES_json = urllib.request.urlopen(reqES, timeout=5).read().decode('utf-8')
                logger.error("respES_json: " + str(respES_json)) 
                esResponse = json.loads(respES_json)
                hitArray = esResponse["hits"]["hits"]
                finalArray = []
                for i in hitArray:
                    iDict = i["_source"]
                    finalArray.append(iDict)
                if request.GET['type'] == 'task':
                    return JsonResponse([finalArray, False, False], safe=False)
                elif request.GET['type'] == 'user':
                    return JsonResponse([False, finalArray, False], safe=False)
                else:
                    return JsonResponse([False, False, finalArray], safe=False)
        else:
            return JsonResponse([[],[],[]], safe=False)
        if not tasks:
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/task/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                tasks = resp
            except URLError:
                tasks = "ERROR: Server Timeout"
        if not users:
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/user/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                logger.error(resp)
                users = resp
            except URLError:
                users = "ERROR: Server Timeout"
        if not reviews:
            try:
                req = urllib.request.Request('http://models-api:8000/api/v1/review/all/')
                resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                resp = json.loads(resp_json)
                logger.error(resp)
                reviews = resp
            except URLError:
                reviews = "Error: ServerTimeout"
        return JsonResponse([tasks, users, reviews], safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def user(request, user_id):
    if request.method == 'GET':
        errorStrings = ""
        try:
            req = urllib.request.Request('http://models-api:8000/api/v1/user/main/' 
                    + user_id + '/')
            resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            resp = json.loads(resp_json)
            return JsonResponse(resp, safe=False)
        except URLError:
            resp = False
            errorStrings = "Timeout Error"
            return HttpResponse("Timeout")
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def review(request, review_id):
    if request.method == 'GET':
        errorStrings = ""
        try:
            req = urllib.request.Request('http://models-api:8000/api/v1/review/info/' 
                    + review_id + '/')
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
                req2 = urllib.request.Request('http://models-api:8000/api/v1/user/info/' 
                        + str(resp["postee_user"]) + '/')
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
                req3 = urllib.request.Request('http://models-api:8000/api/v1/user/info/' 
                        + str(resp["poster_user"]) + '/')
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
                req4 = urllib.request.Request('http://models-api:8000/api/v1/task/info/' 
                        + str(resp["task"]) + '/')
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

def signup(request):
    if request.method == "POST":
        errorStrings = False
        respDict = (request.POST).dict()
        languagesString = respDict['spoken_languages']
        skillsString = respDict['user_skills']
        del respDict['spoken_languages']
        del respDict['user_skills']
        post_encoded = urllib.parse.urlencode(respDict).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/user/create/', 
                data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        try:
            resp = json.loads(resp_json)
        except ValueError:
            return JsonResponse([False, False, resp_json], safe=False)
        #ADD IN KAFKA FOR USERS HERE
        message = json.dumps([resp, 'user']).encode('utf-8')
        kafka_producer = KafkaProducer(bootstrap_servers='kafka_container:9092');
        kafka_producer.send("task_topic", message)
        auth_encoded = urllib.parse.urlencode({"username": resp["username"]}).encode('utf-8')
        req2 = urllib.request.Request('http://models-api:8000/api/v1/authenticator/create/', 
                data=auth_encoded, method='POST')
        resp2_json = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
        try:
            resp2 = json.loads(resp2_json)
        except ValueError:
            resp2 = False
            errorStrings = resp2_json
        if skillsString != "":
            skillsArray = skillsString.split(",")
            for i in skillsArray:
                post_encoded = urllib.parse.urlencode(
                        {'user': resp['id'], 'skill': i}).encode('utf-8')
                req3 = urllib.request.Request('http://models-api:8000/api/v1/userSkills/create/', 
                        data=post_encoded, method='POST')
                resp3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
        if languagesString != "":
            languagesArray = languagesString.split(",")
            for i in languagesArray:
                post_encoded = urllib.parse.urlencode(
                        {'user': resp['id'], 'spoken_language': i}).encode('utf-8')
                req3 = urllib.request.Request(
                        'http://models-api:8000/api/v1/userLanguages/create/', 
                        data=post_encoded, method='POST')
                resp3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')

        return JsonResponse([resp2, resp, errorStrings], safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")

def login(request):
    if request.method == "POST":
        errorStrings = ""
        post_encoded = urllib.parse.urlencode((request.POST).dict()).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/user/find/', 
                data=post_encoded, method='POST')
        resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        if resp == "Correct":
            auth_encoded = urllib.parse.urlencode({"username": request.POST["username"]}).encode('utf-8')
            req2 = urllib.request.Request('http://models-api:8000/api/v1/authenticator/create/', 
                    data=auth_encoded, method='POST')
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
        req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/find/' 
                + request.POST["authenticator"] + '/')
        resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        try: 
            resp = json.loads(resp_json)
        except ValueError:
            return JsonResponse([False, resp_json], safe=False)
        for i in resp:
            delreq = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' 
                    + str(i["authenticator"]) + '/', method="DELETE")
            resp_json = urllib.request.urlopen(delreq, timeout=5).read().decode('utf-8')
        return JsonResponse(["Success", False], safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")

def createListing(request):
    if request.method == "POST":
        respDict = (request.POST).dict()
        auth = respDict["auth"]
        req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' 
                + str(auth) + '/', method="GET")
        resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        if resp == "Auth Incorrect":
            return JsonResponse([False, "ERROR: Invalid Auth"], safe=False)
        del respDict["auth"]
        if respDict["pricing_type"] == "Lump":
            respDict["pricing_type"] = True
        else:
            respDict["pricing_type"] = False
        if respDict["remote"] == "remote":
            respDict["remote"] = True
        else:
            respDict["remote"] = False
        skillsString = respDict["skills"]
        del respDict["skills"]
        post_encoded = urllib.parse.urlencode(respDict).encode('utf-8')
        req2 = urllib.request.Request('http://models-api:8000/api/v1/task/create/', 
                data=post_encoded, method='POST')
        resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
        try:
            resp2 = json.loads(resp_json2)
        except ValueError:
            return JsonResponse([False, resp_json2])
        #  Push json bytes to kafka stream
        response_as_list = list(resp2)
        task_json = response_as_list[0]
        resp2['time_to_live'] = str(resp2['time_to_live'])
        resp2['post_date'] = str(resp2['post_date'])
        logger.error("resp2")
        logger.error(resp2)
        message = json.dumps([resp2, 'task']).encode('utf-8')
        kafka_producer = KafkaProducer(bootstrap_servers='kafka_container:9092');
        kafka_producer.send("task_topic", message)

        if skillsString != "":
            skillsArray = skillsString.split(",")
            for i in skillsArray:
                post_encoded = urllib.parse.urlencode(
                        {'task': resp2['id'], 'skill': i}).encode('utf-8')
                req3 = urllib.request.Request('http://models-api:8000/api/v1/taskSkills/create/'
                        , data=post_encoded, method='POST')
                resp3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
        post_encoded = urllib.parse.urlencode({'task': resp2['id'], 'user': resp}).encode('utf-8')
        req3 = urllib.request.Request('http://models-api:8000/api/v1/taskOwners/create/', 
                data=post_encoded, method='POST')
        resp3 = urllib.request.urlopen(req3, timeout=5).read().decode('utf-8')
        return JsonResponse([resp2, False], safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")

def profile(request, auth):
    req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' + str(auth) + '/', method="GET")
    resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        
    if resp == "Auth Incorrect":
        return JsonResponse([False, False, "ERROR: Invalid Auth"], safe=False)

    req2 = urllib.request.Request('http://models-api:8000/api/v1/user/neededReviews/' + resp + '/', method="GET")
    resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
    try:
        resp2 = json.loads(resp_json2)
    except ValueError:
        return JsonResponse([False, resp, resp_json2])

    return JsonResponse([resp2, resp, False], safe=False)

def createReview(request):
    if request.method == "POST":
        respDict = (request.POST).dict()
        auth = respDict["auth"]
        req = urllib.request.Request('http://models-api:8000/api/v1/authenticator/' 
                + str(auth) + '/', method="GET")
        resp = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        if resp == "Auth Incorrect":
            return JsonResponse([False, "ERROR: Invalid Auth"], safe=False)
        #Check to see that the auth is associated with the 
        #person who is supposed to be posting the review
        if not resp == respDict["poster_user"]:
            return JsonResponse([False, "ERROR: Invalid Auth"], safe=False)
        del respDict["auth"]
        #logger.error(respDict)
        post_encoded = urllib.parse.urlencode(respDict).encode('utf-8')
        req2 = urllib.request.Request('http://models-api:8000/api/v1/review/create/', 
                data=post_encoded, method='POST')
        resp_json2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
        try:
            resp2 = json.loads(resp_json2)
        except:
            return JsonResponse([False, resp_json2], safe=False)
        message = json.dumps([resp2, 'review']).encode('utf-8')
        kafka_producer = KafkaProducer(bootstrap_servers='kafka_container:9092');
        kafka_producer.send("task_topic", message)
        return JsonResponse([resp2, False], safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")



