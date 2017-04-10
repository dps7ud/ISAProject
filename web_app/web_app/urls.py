from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.http import Http404
import django.views.defaults

from . import views

#handler404 = 'views.four_oh_four'
statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    #Since debug==True, need to manualy route to our 404 page
    url(r'^404/?', views.four_oh_four, ),
	url(r'^user/(?P<user_id>[0-9]+)/?$', views.user, name='user'),
    url(r'^task/?$', views.task_all, name='task_all'),
    url(r'^createListing/?', views.create_listing, name='create_listing'),
    url(r'^createReview/?', views.create_review, name='create_review'),
    url(r'^home/?', views.home, name='home'),
    url(r'^login/?', views.login, name='login'),
    url(r'^logout/?', views.logout, name='logout'),
    url(r'^review/(?P<review_id>[0-9]+)/?$', views.review, name='review'),
    url(r'^signup/?', views.signup, name='signup'),
    url(r'^task/(?P<task_id>[0-9]+)/?$', views.task, name='task'),
    url(r'^user/(?P<user_id>[0-9]+)/?$', views.user, name='user'),
    url(r'^profile/?', views.profile, name='profile'),




    url(r'^/?$', views.home, name='home'),
] + statics
