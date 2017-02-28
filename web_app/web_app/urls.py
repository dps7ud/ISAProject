from django.conf.urls import url
from django.http import Http404
import django.views.defaults

from . import views

#handler404 = 'views.four_oh_four'

urlpatterns = [
    #Since debug==True, need to manualy route to our 404 page
    url(r'^404/?', views.four_oh_four, ),
	url(r'^user/(?P<user_id>[0-9]+)/?$', views.user, name='user'),
	url(r'^task/(?P<task_id>[0-9]+)/?$', views.task, name='task'),
    url(r'^review/(?P<review_id>[0-9]+)/?$', views.review, name='review'),
    url(r'^home/?', views.home, name='home'),
    url(r'^/?$', views.home, name='home'),
]
