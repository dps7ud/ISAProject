from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^', views.home, name='home'),
    
]
