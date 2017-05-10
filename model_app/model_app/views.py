from django.contrib.auth import hashers
from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.utils import timezone

from .models import *

import hmac
import datetime
import json
import logging
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    template = loader.get_template('home/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def authenticator_create(request):
    if request.method == 'POST':
        auth_obj = Authenticator()
        required = {'username'}
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        for key, value in request.POST.items():
            setattr(auth_obj, key, value)
        authValid = True
        newAuth = "placeholder"
        while authValid:
            newAuth = hmac.new(
                key = settings.SECRET_KEY.encode('utf-8'),
                msg = os.urandom(32),
                digestmod = 'sha256',
            ).hexdigest()
            try:
                Authenticator.objects.get(authenticator=newAuth)
            except Authenticator.DoesNotExist:
                authValid = False
        auth_obj.authenticator = newAuth
        auth_obj.date_created = timezone.now()    
        auth_obj.save()
        print("New Auth")
        print (auth_obj.authenticator)
        return JsonResponse(model_to_dict(auth_obj))
    else:
        return HttpResponse("ERROR: Endpoint must be POSTed")

def authenticator_find(request, authenticator):
    if request.method == 'GET':
        logger.error("Auth Finder")
        try:
            authOrig = Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            return HttpResponse("ERROR: Authenticator does not exist")
        logger.error(authOrig)
        auths = Authenticator.objects.filter(username=str(authOrig.username)) 
        authsList = []
        for i in auths:
            authsList.append(model_to_dict(i))
        logger.error(authsList)
        return JsonResponse(authsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def authenticator(request, authenticator):
    if request.method == 'GET':
        try:
            authObj = Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            return HttpResponse("Auth Incorrect")
        if authObj.date_created <= timezone.now() - datetime.timedelta(days=7):
            logger.error("Auth is too old")
            #authObj.delete()
            return HttpResponse("Auth Incorrect")
        userObj = Users.objects.get(username=authObj.username)
        return HttpResponse(str(userObj.pk))
    elif request.method == 'DELETE':
        logger.error("delete")
        logger.error(authenticator)
        try:
            authObj = Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            return HttpResponse("ERROR: Authenticator with that id does not exist")
        try:
            authObj.delete()
            return HttpResponse("Deleted Authenticator: " + str(authenticator))
        except:
            return HttpResponse("Authenticator Deletion failed")
    else:
        return HttpResponse("ERROR: Not correct type of Request")

def review_info(request, review_id):
    """Used to retrieve, update, and delete a review which is already created
        GET: Returns review with *review_id* if it exists, error otherwise
        POST: Updates fields for review with *review_id*, returns error if no such review
    """

    if request.method == 'POST':
        try:
            reviewObj = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return HttpResponse("ERROR: Review with that id does not exist")
        json_data = request.POST
        if 'body' in json_data:
            reviewObj.body = json_data['body']
        if 'title' in json_data:
            reviewObj.title = json_data['title']
        if 'score' in json_data:
            reviewObj.score = float(json_data['score'])
        if 'task' in json_data:
            try:
                reviewObj.task = Task.objects.get(pk=json_data['task'])
            except Task.DoesNotExist:
                return HttpResponse("ERROR: Task object does not exist")
        if 'poster_user' in json_data:
            try:
                reviewObj.poster_user = Users.objects.get(pk=json_data['poster_user'])
            except Users.DoesNotExist:
                return HttpResponse("ERROR: Poster User does not exist")
        if 'postee_user' in json_data:
            try:
                reviewObj.postee_user = Users.objects.get(pk=json_data['postee_user'])
            except Users.DoesNotExist:
                return HttpResponse("ERROR: Postee User does not exist")
        try:
            reviewObj.save()
            return JsonResponse(model_to_dict(reviewObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")      
    elif request.method == 'DELETE':
        try:
            reviewObj = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return HttpResponse("ERROR: Review with that id does not exist")
        reviewObj.delete()
        return HttpResponse("Deleted Review with ID: " + str(review_id))
    else:
        try:
            reviewObj = Review.objects.get(pk=review_id)
            return JsonResponse(model_to_dict(reviewObj))
        except Review.DoesNotExist:
            return HttpResponse("ERROR: Review with that id does not exist")

def review_create(request):
    if request.method == 'POST':

        required = {'task','poster_user','postee_user'}
        reviewObj = Review()
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        for key, value in json_data.items():
            #ugly
            if key not in required:
                setattr(reviewObj, key, value)        
        # Any field not specified in the body of the request will 
        #use the default value of the review
        if 'task' in json_data:
            try:
                reviewObj.task = Task.objects.get(pk=json_data['task'])
            except Task.DoesNotExist:
                return HttpResponse("ERROR: Task object does not exist")
        if 'poster_user' in json_data:
            try:
                reviewObj.poster_user = Users.objects.get(pk=json_data['poster_user'])
            except Users.DoesNotExist:
                return HttpResponse("ERROR: Poster User does not exist")
        if 'postee_user' in json_data:
            try:
                reviewObj.postee_user = Users.objects.get(pk=json_data['postee_user'])
            except Users.DoesNotExist:
                return HttpResponse("ERROR: Postee User does not exist")
        try:
            reviewObj.save()
            return JsonResponse(model_to_dict(reviewObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")  
    else:
        return HttpResponse("ERROR: Review Creation endpoint must be POSTed") 

def review_all(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        reviewsList = []
        for i in reviews:
            reviewsList.append(model_to_dict(i))
        return JsonResponse(reviewsList, safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")


def task_query(request):
    """ Allows GET requests to access model instances by filtering"""
    if request.method == 'GET':
        query_dict = { key:request.GET[key] for key in request.GET}
        try:
            tasks = Task.objects.filter(**query_dict)
            data = serializers.serialize("json", tasks)
        except Task.DoesNotExist:
            data = "Data not found"
        except ValidationError:
            data = "Lets pretend this is graceful"
        return HttpResponse(data)
    else:
        return HttpResponse("ERROR: Posted to task_query")

def task_all(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasksList = []
        for i in tasks:
            tasksList.append(model_to_dict(i))
        return JsonResponse(tasksList, safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")

def task_create(request):
    """Accepts post request containing a single json object
    to create new task model instances.
    """
    if request.method == "POST":
        required = set(field.name for field in set(Task._meta.fields))
        required.remove('id')
        required.remove('time_to_live')
        required.remove('post_date')

        try:
            request_data = request.POST
        except ValueError:
            HttpResponse("Bad json input, it's super pickey for some reason. I promise it works.")
        missing_fields = required.difference(request_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        task_obj = Task()
        for key, value in request_data.items():
            setattr(task_obj, key, value)
        task_obj.time_to_live = timezone.now() + datetime.timedelta(days=30)
        task_obj.post_date = datetime.datetime.now()      
        task_obj.save()
        return JsonResponse(model_to_dict(task_obj))
    else:
        return HttpResponse("ERROR: task_create must be POSTed")

def task_info(request, task_id):
    """Used to get, update and delete task objects.
       Returns error if no such task exists.
        -GET return json task object
        -POST update a task and reports success of update
        -DELETE deletes object with specified *task_id*
    """
    try:
        task_obj = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponse("ERROR: Task with that id does not exist")
    if request.method == "GET":
        return JsonResponse(model_to_dict(task_obj))
    elif request.method == "POST":
        try:
            update_data = request.POST
        except ValueError:
            return HttpResponse("ERROR: Bad POST body")
        for key, value in update_data.items():
            setattr(task_obj, key, value)
        task_obj.save()
        return HttpResponse("Updated task with id: " + str(task_obj.pk))
    elif request.method == "DELETE":
        task_obj.delete()
        return HttpResponse("Deleted Task with ID: " + str(task_id))
    else:
        return HttpResponse("pass\n")

def user_info(request, user_id):
    """Used to retrieve, update and delete a user
        GET: Returns user with *user_id* if it exists, error otherwise
        POST: Updates fields for user with *user_id*, returns error if no such user
    """
    if request.method == 'POST':
        try:
            userObj = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User with that id does not exist")
        json_data = request.POST
        logger.error("In the models layer")
        logger.error(json_data)
        if 'username' in json_data:
            userObj.username = json_data['username']
        if 'fname' in json_data:
            userObj.fname = json_data['fname']
        if 'lname' in json_data:
            userObj.lname = json_data['lname']
        if 'email' in json_data:
            userObj.email = json_data['email']
        if 'bio' in json_data:
            userObj.bio = json_data['bio']
        if 'pw' in json_data:
            userObj.pw = json_data['pw']
        if 'location' in json_data:
            userObj.location = json_data['location']
        try:
            userObj.save()
            return JsonResponse(model_to_dict(userObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")  
    elif request.method == 'DELETE':
        try:
            userObj = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User with that id does not exist")
        userObj.delete()
        return HttpResponse("Deleted User with ID: " + str(user_id))
    else:
        try:
            userObj = Users.objects.get(pk=user_id)
            return JsonResponse(model_to_dict(userObj))
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User with that id does not exist")

def user_create(request):
    if request.method == 'POST':
        required = set(field.name for field in set(Users._meta.fields))
        required.remove('id')
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return JsonResponse({"ERROR":"Missing required fields: " + ', '.join(missing_fields)})
        userObj = Users()
        for key, value in json_data.items():
            if key == 'pw':
                setattr(userObj, key, hashers.make_password(json_data['pw']))
            else:
                setattr(userObj, key, value)
        try:
            Users.objects.get(username=userObj.username)
        except Users.DoesNotExist:
            userObj.save()
            return JsonResponse(model_to_dict(userObj))
        return HttpResponse("ERROR: Username already registered")
    else:
        return HttpResponse("ERROR: User creation endpoint must be posted")

def user_find(request):
    if request.method == 'POST':
        try:
            userObj = Users.objects.get(username=request.POST['username'])
        except Users.DoesNotExist:
            return HttpResponse("Username not registered")

        if hashers.check_password(request.POST['pw'], userObj.pw):
            return HttpResponse("Correct")
        else:
            return HttpResponse("Password Incorrect")
    else:
        return HttpResponse("ERROR: Endpoint only accepts POST requests")

def user_all(request):
    if request.method == 'GET':
        users = Users.objects.all()
        usersList = []
        for i in users:
            usersList.append(model_to_dict(i))
        return JsonResponse(usersList, safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")


# ----------------------- For Project 3 ------------------------------------
def user_rating(user):
    reviews = Review.objects.filter(postee_user=user.id)
    count = 0;
    total = 0;
    for i in reviews:
        count += 1;
        total += i.score
    if count == 0:
        return 0
    else:
        return total/count

def get_user_rating(request, user_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(postee_user=user_id)
        count = 0;
        total = 0;
        for i in reviews:
            count += 1;
            total += i.score
        if count == 0:
            return JsonResponse({"rating": 0})
        else:
            return JsonResponse({"rating": total/count})
    else:
        return HttpResponse("ERROR: Can only accept GET requests")       


def get_top_users(request):
    if request.method == 'GET':
        users = Users.objects.all()
        users = (sorted(users, key=user_rating, reverse=True))[:5]
        usersList = []
        for i in users:
            usersList.append(model_to_dict(i))
        return JsonResponse(usersList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")
    

def get_recent_listings(request):
    if request.method == 'GET':
        latest_listings = Task.objects.order_by('-post_date')[:5]
        listingsList = []
        for i in latest_listings:
            listingsList.append(model_to_dict(i))
        return JsonResponse(listingsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")
    

def task_skills(request, task_id):
    if request.method == 'GET':
        skills = TaskSkills.objects.filter(task=task_id)
        skillsList = []
        for i in skills:
            skillsList.append(model_to_dict(i))
        return JsonResponse(skillsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def task_skills_create(request):
    if request.method == 'POST':
        skillsObj = TaskSkills()
        required = {'task','skill'}
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        try:
            skillsObj.task = Task.objects.get(pk=json_data['task'])
        except Task.DoesNotExist:
            return HttpResponse("ERROR: Task object does not exist")
        skillsObj.skill = json_data['skill']
        try:
            skillsObj.save()
            return JsonResponse(model_to_dict(skillsObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")
    else:
        return HttpResponse("ERROR: Can only accept POST requests")

def task_owners(request, task_id):
    if request.method == 'GET':
        owners = Users.objects.filter(owner__task=task_id)
        ownersList = []
        for i in owners:
            ownersList.append(model_to_dict(i))
        return JsonResponse(ownersList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def task_owners_create(request):
    if request.method == 'POST':
        ownerObj = Owner()
        required = {'task','user'}
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        try:
            ownerObj.task = Task.objects.get(pk=json_data['task'])
        except Task.DoesNotExist:
            return HttpResponse("ERROR: Task object does not exist")
        try:
            ownerObj.user = Users.objects.get(pk=json_data['user'])
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User object does not exist")
        try:
            ownerObj.save()
            return JsonResponse(model_to_dict(ownerObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")
    else:
        return HttpResponse("ERROR: Can only accept POST requests")
    

def task_workers(request, task_id):
    if request.method == 'GET':
        workers = Users.objects.filter(worker__task=task_id)
        workersList = []
        for i in workers:
            workersList.append(model_to_dict(i))
        return JsonResponse(workersList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def task_reviews(request, task_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(task=task_id)
        reviewsList = []
        for i in reviews:
            reviewsList.append(model_to_dict(i))
        return JsonResponse(reviewsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def user_languages(request, user_id):
    if request.method == 'GET':
        languages = UserLanguages.objects.filter(user=user_id)
        languagesList = []
        for i in languages:
            languagesList.append(model_to_dict(i))
        return JsonResponse(languagesList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")
    

def user_languages_create(request):
    if request.method == 'POST':
        langObj = UserLanguages()
        required = {'spoken_language','user'}
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        try:
            langObj.user = Users.objects.get(pk=json_data['user'])
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User object does not exist")
        langObj.spoken_language = json_data['spoken_language']
        try:
            langObj.save()
            return JsonResponse(model_to_dict(langObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")
    else:
        return HttpResponse("ERROR: Can only accept POST requests")

def user_skills(request, user_id):
    if request.method == 'GET':
        skills = UserSkills.objects.filter(user=user_id)
        skillsList = []
        for i in skills:
            skillsList.append(model_to_dict(i))
        return JsonResponse(skillsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def user_skills_create(request):
    if request.method == 'POST':
        required = {'skill','user'}
        json_data = request.POST
        missing_fields = required.difference(json_data.keys())
        if missing_fields:
            return HttpResponse("Missing required fields: " + ', '.join(missing_fields))
        skillsObj = UserSkills()
        try:
            skillsObj.user = Users.objects.get(pk=json_data['user'])
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User object does not exist")
        skillsObj.skill = json_data['skill']
        try:
            skillsObj.save()
            return JsonResponse(model_to_dict(skillsObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")
    else:
        return HttpResponse("ERROR: Can only accept POST requests")

def user_owner_tasks(request, user_id):
    if request.method == 'GET':
        tasks = Task.objects.filter(owner__user=user_id)
        tasksList = []
        for i in tasks:
            tasksList.append(model_to_dict(i))
        return JsonResponse(tasksList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def user_worker_tasks(request, user_id):
    if request.method == 'GET':
        tasks = Task.objects.filter(worker__user=user_id)
        tasksList = []
        for i in tasks:
            tasksList.append(model_to_dict(i))
        return JsonResponse(tasksList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def user_reviews(request, user_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(poster_user=user_id)
        reviewsList = []
        for i in reviews:
            reviewsList.append(model_to_dict(i))
        return JsonResponse(reviewsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")
    

def user_reviewed(request, user_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(postee_user=user_id)
        reviewsList = []
        for i in reviews:
            reviewsList.append(model_to_dict(i))
        return JsonResponse(reviewsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

def user_main(request, user_id):
    responseArray = []
    errorString = ""
    try:
        userObj = Users.objects.get(pk=user_id)
        responseArray.append(model_to_dict(userObj))
    except Users.DoesNotExist:
        errorString += "ERROR: User with that id does not exist"
        responseArray.append(False)

    languages = UserLanguages.objects.filter(user=user_id)
    languagesList = []
    for i in languages:
        languagesList.append(model_to_dict(i))
    responseArray.append(languagesList)

    skills = UserSkills.objects.filter(user=user_id)
    skillsList = []
    for i in skills:
        skillsList.append(model_to_dict(i))
    responseArray.append(skillsList)

    tasks = Task.objects.filter(owner__user=user_id)
    tasksList = []
    for i in tasks:
        tasksList.append(model_to_dict(i))
    responseArray.append(tasksList)

    tasks = Task.objects.filter(worker__user=user_id)
    tasksList = []
    for i in tasks:
        tasksList.append(model_to_dict(i))
    responseArray.append(tasksList)

    reviews = Review.objects.filter(poster_user=user_id)
    reviewsList = []
    for i in reviews:
        reviewsList.append(model_to_dict(i))
    responseArray.append(reviewsList)

    reviews = Review.objects.filter(postee_user=user_id)
    reviewsList = []
    for i in reviews:
        reviewsList.append(model_to_dict(i))
    responseArray.append(reviewsList)

    responseArray.append(errorString)

    return JsonResponse(responseArray, safe=False)

def task_main(request, task_id):
    responseArray = []
    errorString = ""

    try:
        taskObj = Task.objects.get(pk=task_id)
        responseArray.append(model_to_dict(taskObj))
    except Task.DoesNotExist:
        errorString += "ERROR: Task with that id does not exist"
        responseArray.append(False)

    skills = TaskSkills.objects.filter(task=task_id)
    skillsList = []
    for i in skills:
        skillsList.append(model_to_dict(i))
    responseArray.append(skillsList)

    owners = Users.objects.filter(owner__task=task_id)
    ownersList = []
    for i in owners:
        ownersList.append(model_to_dict(i))
    responseArray.append(ownersList)

    workers = Users.objects.filter(worker__task=task_id)
    workersList = []
    for i in workers:
        workersList.append(model_to_dict(i))
    responseArray.append(workersList)

    reviews = Review.objects.filter(task=task_id)
    reviewsList = []
    for i in reviews:
        reviewsList.append(model_to_dict(i))
    responseArray.append(reviewsList)

    recommendationList = []
    recommendation1 = Task.objects.filter(recommendation_second__task_first=task_id)
    for i in recommendation1:
        newReco = model_to_dict(i)
        if str(newReco['id']) != str(task_id):
            recommendationList.append(newReco)
    recommendation2 = Task.objects.filter(recommendation_first__task_second=task_id)
    for j in recommendation2:
        newReco = model_to_dict(j)
        if str(newReco['id']) != str(task_id):
            recommendationList.append(newReco)
    responseArray.append(recommendationList)


    responseArray.append(errorString)
    logger.error("responseArray")
    logger.error(responseArray)
    return JsonResponse(responseArray, safe=False)

def get_user_needed_reviews(request, user_id):
    if request.method == "GET":
        logger.error("user_id")
        logger.error(user_id)
        needed_pairs = []
        tasks = Task.objects.filter(worker__user=user_id)
        logger.error(tasks)
        for i in tasks:
            workers = Users.objects.filter(worker__task=i.pk)
            for j in workers:
                if int(j.pk) != int(user_id):
                    logger.error("j.pk")
                    logger.error(j.pk)
                    try:
                        reviewAttempts = Review.objects.get(task=i.pk, postee_user=j.pk, poster_user=user_id)
                    except Review.DoesNotExist:
                        needed_pairs.append([model_to_dict(i), model_to_dict(j)])
            owners = Users.objects.filter(owner__task = i.pk)
            for j in owners:
                if int(j.pk) != int(user_id):
                    logger.error("j.pk")
                    logger.error(j.pk)
                    try:
                        reviewAttempts = Review.objects.get(task=i.pk, postee_user=j.pk, poster_user=user_id)
                    except Review.DoesNotExist:
                        needed_pairs.append([model_to_dict(i), model_to_dict(j)])
        tasks = Task.objects.filter(owner__user=user_id)
        for i in tasks:
            workers = Users.objects.filter(worker__task=i.pk)
            for j in workers:
                if int(j.pk) != int(user_id):
                    logger.error("j.pk")
                    logger.error(j.pk)
                    try:
                        reviewAttempts = Review.objects.get(task=i.pk, postee_user=j.pk, poster_user=user_id)
                    except Review.DoesNotExist:
                        needed_pairs.append([model_to_dict(i), model_to_dict(j)])
            owners = Users.objects.filter(owner__task = i.pk)
            for j in owners:
                if int(j.pk) != int(user_id):
                    logger.error("j.pk")
                    logger.error(j.pk)
                    try:
                        reviewAttempts = Review.objects.get(task=i.pk, postee_user=j.pk, poster_user=user_id)
                    except Review.DoesNotExist:
                        needed_pairs.append([model_to_dict(i), model_to_dict(j)])
        return JsonResponse(needed_pairs, safe=False)
    else:
        return HttpResponse("ERROR: Endpoint only accepts GET requests")
