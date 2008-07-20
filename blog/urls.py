#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.blog.views',
	# main page of blog
	(r'^$', 'get_latest_entries'),
	# archives for blogs..
	(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'get_entries_for_day'),
	# an entry on a specific date
	(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'get_post'),
	# entries with the specified tag
	(r'^tags/(?P<tag>[\s\w\d]+)/$', 'get_entries_for_tag'),
	# search against entries
	(r'^search/$', 'search'),
)
