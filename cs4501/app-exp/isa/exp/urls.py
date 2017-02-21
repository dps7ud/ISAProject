from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),

    
]
