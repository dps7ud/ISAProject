from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^api/v1/review/create/$', views.review_create, name='review_create'),
    url(r'^api/v1/task/.*', views.task, name='task'),
]
