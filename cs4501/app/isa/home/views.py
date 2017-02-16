from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import Review, Task, Users

import json

# Create your views here.
def index(request):
    template = loader.get_template('home/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def review(request, review_id):
    if request.method == 'POST':
        try:
            reviewObj = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            reviewObj = Review()
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        if 'body' in json_data:
            reviewObj.body = json_data['body']
        if 'title' in json_data:
            reviewObj.title = json_data['title']
        if 'score' in json_data:
            reviewObj.score = json_data['score']
        if 'task_id' in json_data:
            review.task_id = json_data['task_id']
        if 'poster_user_id' in json_data:
            reviewObj.poster_user_id = json_data['poster_user_id']
        if 'postee_user_id' in json_data:
            reviewObj.postee_user_id = json_data['postee_user_id']
        try:
            reviewObj.save()
            data = serializers.serialize("json", [reviewObj])
        except:
            data = "ERROR: Wrong data type inputs"      
        return HttpResponse(data)
    else:
        try:
            reviewObj = Review.objects.get(pk=review_id)
            data = serializers.serialize("json", [reviewObj])
        except Review.DoesNotExist:
            data = "ERROR: Review with that id does not exist"
        return HttpResponse(data)

@csrf_exempt
def review_create(request):
    reviewObj = Review()
    #count = Review.objects.get().count()
    #reviewObj.review_id = count+1
    body_unicode = request.body.decode('utf-8')
    json_data = json.loads(body_unicode)
    if 'body' in json_data:
        reviewObj.body = json_data['body']
    if 'title' in json_data:
        reviewObj.title = json_data['title']
    if 'score' in json_data:
        reviewObj.score = json_data['score']
    if 'task_id' in json_data:
        review.task_id = json_data['task_id']
    if 'poster_user_id' in json_data:
        reviewObj.poster_user_id = json_data['poster_user_id']
    if 'postee_user_id' in json_data:
        reviewObj.postee_user_id = json_data['postee_user_id']
    try:
        reviewObj.save()
        data = serializers.serialize("json", [reviewObj])
    except :
        data = "ERROR: Wrong data type inputs"
    return HttpResponse(data)

@csrf_exempt
def task(request):
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
        return HttpResponse(False)

@csrf_exempt
def task_create(request):
    """Accepts post request containing a single json object
    to create new task model instances. Acceptable json looks like this:
    {
        "task_id":"4",
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
        required = tuple(field.name for field in Task._meta.get_fields())
        try:
            request_body = request.body.decode('utf-8')
            request_data = json.loads(request_body)
        except ValueError:
            HttpResponse("Bad json input, it's super pickey for some reason. I promise it works.")
        for requirement in required:
            if requirement not in request_data:
                return HttpResponse(str(requirement) + " is a required field.")
        primary_keys = []
        task_obj = Task(**request_data)
        task_obj.save()
        return HttpResponse("Created object with id: " + str(task_obj.task_id))
    else:
        return HttpResponse(False)

@csrf_exempt
def task_info(request, task_id):
    """Get requests return an individual object, post requests update
    an individual object and reports success of update"""
    try:
        task_obj = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponse(False)
    if request.method == "GET":
        data = serializers.serialize("json", [task_obj])
        return HttpResponse(data)
    elif request.method == "POST":
        request_body = request.body.decode('utf-8')
        try:
            update_data = json.loads(request_body)
        except ValueError:
            return HttpResponse(False)
        for key, value in update_data.items():
            setattr(task_obj, key, value)
        task_obj.save()
        return HttpResponse(True)
    else:
        return HttpResponse("pass\n")

@csrf_exempt
def user(request, user_id):
    if request.method == 'POST':
        try:
            userObj = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            userObj = Users()
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        if 'fname' in json_data:
            userObj.fname = json_data['fname']
        if 'lname' in json_data:
            userObj.lname = json_data['lname']
        if 'email' in json_data:
            userObj.email = json_data['email']
        if 'bio' in json_data:
            user.bio = json_data['bio']
        if 'pw' in json_data:
            userObj.pw = json_data['pw']
        if 'location' in json_data:
            userObj.location = json_data['location']
        try:
            userObj.save()
            data = serializers.serialize("json", [userObj])
        except:
            data = "ERROR: Wrong data type inputs"      
        return HttpResponse(data)
    else:
        try:
            userObj = Users.objects.get(pk=user_id)
            data = serializers.serialize("json", [userObj])
        except Users.DoesNotExist:
            data = "ERROR: User with that id does not exist"
            #return HttpResponse("You're looking at User %s." % User_id)
        return HttpResponse(data)

@csrf_exempt
def user_create(request):
    userObj = Users()
    #count = User.objects.get().count()
    #UserObj.User_id = count+1
    body_unicode = request.body.decode('utf-8')
    json_data = json.loads(body_unicode)
    if 'fname' in json_data:
        userObj.fname = json_data['fname']
    if 'lname' in json_data:
        userObj.lname = json_data['lname']
    if 'email' in json_data:
        userObj.email = json_data['email']
    if 'bio' in json_data:
        user.bio = json_data['bio']
    if 'pw' in json_data:
        userObj.pw = json_data['pw']
    if 'location' in json_data:
        userObj.location = json_data['location']
    try:
        userObj.save()
        data = serializers.serialize("json", [userObj])
    except :
        data = "ERROR: Wrong data type inputs"
    return HttpResponse(data)
