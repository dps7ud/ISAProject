from django.shortcuts import render
from django.http import HttpResponse
#from django.http import JsonReponse
from django.template import loader
from django.core import serializers

from .models import Review
import json

# Create your views here.
def index(request):
	template = loader.get_template('home/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def review(request, review_id):
	if request.method == 'POST':
		reviewObj = Review.object.get(pk=review_id)
		json_data = json.loads(request.raw_post_data)
		return HttpResponse(json_data)
	else:
		reviewObj = Review.objects.get(pk=review_id)
		data = serializers.serialize("json", [reviewObj])

		#return HttpResponse("You're looking at review %s." % review_id)
		return HttpResponse(data)