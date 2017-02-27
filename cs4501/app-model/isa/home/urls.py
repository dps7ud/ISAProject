from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^api/v1/review/create/$', views.review_create, name='review_create'),
    url(r'^api/v1/task/info/(?P<task_id>[0-9]+)/$', views.task_info, name='task_info'),
    url(r'^api/v1/task/create/$', views.task_create, name='task_create'),
    url(r'^api/v1/task/query', views.task_query, name='task_query'),
    url(r'^api/v1/user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^api/v1/user/create/$', views.user_create, name='user_create'),
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
