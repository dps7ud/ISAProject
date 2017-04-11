"""exp_app URL Configuration

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
    url(r'^home/$', views.home, name='home'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'^task/$', views.task_all, name='task_all'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^user/$', views.user_all, name='user_all'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^createListing/$', views.createListing, name='create_listing'),
    url(r'^createReview/$', views.createReview, name='create_review'),
    url(r'^profile/(?P<auth>\w+)/$$', views.profile, name='profile'),
    url(r'^admin/', admin.site.urls),
]
