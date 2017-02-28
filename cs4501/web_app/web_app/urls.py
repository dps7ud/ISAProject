from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
	url(r'^task/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^', views.home, name='home'),
    
]
