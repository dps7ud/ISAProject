from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Review, Task, Users, TaskSkills, Owner, Worker, UserLanguages, UserSkills

import json

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    template = loader.get_template('home/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def review(request, review_id):
    if request.method == 'POST':
        try:
            reviewObj = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return HttpResponse("ERROR: Review with that id does not exist")
        # body_unicode = request.body.decode('utf-8')
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

        reviewObj = Review()
        json_data = request.POST
        if 'task' not in json_data:
            return HttpResponse("ERROR: Task field must be specified for Review Creation")
        if 'poster_user' not in json_data:
            return HttpResponse("ERROR: Poster_User field must be specified for Review Creation")
        if 'postee_user' not in json_data:
            return HttpResponse("ERROR: Postee_user field must be specified for Review creation")
        #Any field not specified in the body of the request will use the default value of the review
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
            # logger.error(key)
            # logger.error(Users.objects.get(pk=key))
            #reviewObj.postee_user = json_data['postee_user']
        #try:
        try:
            reviewObj.save()
            return JsonResponse(model_to_dict(reviewObj))
        except:
            return HttpResponse("ERROR: Wrong data type inputs")  
    else:
        return HttpResponse("ERROR: Review Creation endpoint must be POSTed") 

# def review_delete(request, review_id):
#     if request.method == 'DELETE':
#         try:
#             reviewObj = Review.objects.get(pk=review_id)
#         except Review.DoesNotExist:
#             return HttpResponse("ERROR: Review with that id does not exist")
#         reviewObj.delete()
#         return HttpResponse("Deleted Review with ID: " + str(review_id))
#     else :
#         return HttpResponse("ERROR: Review deletion endpoint only accepts DELETE requests")


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


def task_create(request):
    """Accepts post request containing a single json object
    to create new task model instances. Acceptable json looks like this:
    {
        "pricing_info":"0.0",
        "title":"mynew_task",
        "description":"",
        "location":"here",
        "time_to_live":"2017-02-15",
        "post_date":"2017-02-15",
        "status":"OPEN",
        "remote":false,
        "pricing_type":true,
        "time":5
    }
    """
    if request.method == "POST":
        required = set(field.name for field in set(Task._meta.fields).difference({'id'}))
        required.remove('id')

        try:
            # request_body = request.body.decode('utf-8')
            request_data = request.POST
        except ValueError:
            HttpResponse("Bad json input, it's super pickey for some reason. I promise it works.")
        for requirement in required:
            if requirement not in request_data:
                return HttpResponse(str(requirement) + " is a required field.")
        primary_keys = []
        task_obj = Task()
        for key, value in request_data.items():
            setattr(task_obj, key, value)        
        task_obj.save()
        return JsonResponse(model_to_dict(task_obj))
    else:
        return HttpResponse("ERROR: task_create must be POSTed")


def task_info(request, task_id):
    """Get requests return an individual object, post requests update
    an individual object and reports success of update"""
    try:
        task_obj = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponse("ERROR: Task with that id does not exist")
    if request.method == "GET":
        return JsonResponse(model_to_dict(task_obj))
    elif request.method == "POST":
        # request_body = request.body.decode('utf-8')
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


def user(request, user_id):
    if request.method == 'POST':
        try:
            userObj = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return HttpResponse("ERROR: User with that id does not exist")
        # body_unicode = request.body.decode('utf-8')
        json_data = request.POST
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
        userObj = Users()
        #count = User.objects.get().count()
        #UserObj.User_id = count+1
        json_data = request.POST
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
    else:
        return HttpResponse("ERROR: User creation endpoint must be posted")

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

def task_owners(request, task_id):
    if request.method == 'GET':
        owners = Users.objects.filter(owner__task=task_id)
        ownersList = []
        for i in owners:
            ownersList.append(model_to_dict(i))
        return JsonResponse(ownersList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")
    

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
    

def user_skills(request, user_id):
    if request.method == 'GET':
        skills = UserSkills.objects.filter(user=user_id)
        skillsList = []
        for i in skills:
            skillsList.append(model_to_dict(i))
        return JsonResponse(skillsList, safe=False)
    else:
        return HttpResponse("ERROR: Can only accept GET requests")

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





