#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.users.views',
	# register page
	url(r'^register/$', 'register', name='registration'),
	# login page
	url(r'^login/$', 'user_login', name='login_page'),
	# logout page
	url(r'^logout/$', 'user_logout', name='logout_page'),
	# activation page
	url(r'^(?P<username>[\w\d]+)/activate/(?P<key>[\w\d]+)/$', 'activation', name='activation_page'),
	# gravatar request
	url(r'^(?P<username>[\w\d]+)/profile/gravatar/$', 'gravatar', name='gravatar_request'),
	# profile page
	url(r'^(?P<username>[\w\d]+)/profile/$', 'profile', name='profile_page'),
	# profile page notification removal
	url(r'^(?P<username>[\w\d]+)/profile/notification/remove/$', 'notification_remove', name='notification_removal'),
)
