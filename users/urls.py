#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.users.views',
	# register page
	(r'^register/$', 'register'),
	# login page
	(r'^login/$', 'user_login'),
	# logout page
	(r'^logout/$', 'user_logout'),
	# activation page
	(r'^(?P<username>[\w\d]+)/activate/(?P<key>[\w\d]+)/$', 'activation'),
	# gravatar request
	(r'^(?P<username>[\w\d]+)/profile/gravatar/$', 'gravatar'),
	# profile page
	(r'^(?P<username>[\w\d]+)/profile/$', 'profile'),
	# profile page notification removal
	(r'^(?P<username>[\w\d]+)/profile/notification/remove/$', 'notification_remove'),
)
