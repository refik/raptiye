#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.comments.views',
	# comment is sent
	url(r'^sent/$', 'comment_sent', name='comment_sent'),
	# new captcha is requested
	url(r'^new_captcha/$', 'new_captcha', name='new_captcha'),
)
