#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.comments.views',
	# comment is sent
	(r'^sent/$', 'comment_sent'),
	# new captcha is requested
	(r'^new_captcha/$', 'new_captcha'),
)
