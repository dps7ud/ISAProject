from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import Review
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
			#return HttpResponse("You're looking at review %s." % review_id)
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

#@csrf_exempt
#def task(request):
#    if request.method == 'POST':
#        task_obj = Task()
#	    body_unicode = request.body.decode('utf-8')
#	    json_data = json.loads(body_unicode)
#    elif request.method == 'GET':
#        pass
#    return 0

    


