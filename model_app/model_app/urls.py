"""model_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^api/v1/authenticator/create/$', views.authenticator_create, name='authenticator_create'),
    #Username only looks for alphanumeric characters, may need to restrict front end username in the future
    url(r'^api/v1/authenticator/find/(?P<username>\w+)/$', views.authenticator_find, name='authenticator_find'),
    url(r'^api/v1/authenticator/(?P<authenticator>\w+)/$', views.authenticator, name='authenticator'),
    url(r'^api/v1/review/info/(?P<review_id>[0-9]+)/$', views.review_info, name='review_info'),
    url(r'^api/v1/review/create/$', views.review_create, name='review_create'),
    url(r'^api/v1/task/info/(?P<task_id>[0-9]+)/$', views.task_info, name='task_info'),
    url(r'^api/v1/task/main/(?P<task_id>[0-9]+)/$', views.task_main, name='task_main'),
    url(r'^api/v1/task/create/$', views.task_create, name='task_create'),
    url(r'^api/v1/task/query', views.task_query, name='task_query'),
    url(r'^api/v1/user/info/(?P<user_id>[0-9]+)/$', views.user_info, name='user_info'),
    url(r'^api/v1/user/main/(?P<user_id>[0-9]+)/$', views.user_main, name='user_main'),
    url(r'^api/v1/user/create/$', views.user_create, name='user_create'),
    url(r'^api/v1/user/find/$', views.user_find, name='user_find'),
    url(r'^topUsers/$', views.get_top_users, name='get_top_five_users'),
    url(r'^getUserRating/(?P<user_id>[0-9]+)/$', views.get_user_rating, name='get_user_rating'),
    url(r'^recentListings/$', views.get_recent_listings, name='get_recent_listings'),
    url(r'^api/v1/taskSkills/(?P<task_id>[0-9]+)/$', views.task_skills, name='task_skills'),
    url(r'^api/v1/taskOwners/(?P<task_id>[0-9]+)/$', views.task_owners, name='task_owners'),
    url(r'^api/v1/taskWorkers/(?P<task_id>[0-9]+)/$', views.task_workers, name='task_workers'),
    url(r'^api/v1/taskReviews/(?P<task_id>[0-9]+)/$', views.task_reviews, name='task_reviews'),
    url(r'^api/v1/userLanguages/(?P<user_id>[0-9]+)/$', views.user_languages, name='user_languages'),
    url(r'^api/v1/userSkills/(?P<user_id>[0-9]+)/$', views.user_skills, name='user_skills'),
    url(r'^api/v1/userOwnerTasks/(?P<user_id>[0-9]+)/$', views.user_owner_tasks, name='user_owner_tasks'),
    url(r'^api/v1/userWorkerTasks/(?P<user_id>[0-9]+)/$', views.user_worker_tasks, name='user_worker_tasks'),
    url(r'^api/v1/userReviews/(?P<user_id>[0-9]+)/$', views.user_reviews, name='user_reviews'),
    url(r'^api/v1/userReviewed/(?P<user_id>[0-9]+)/$', views.user_reviewed, name='user_reviewed'),
]
