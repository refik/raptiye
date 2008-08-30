#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.blog.views',
	# main page of blog
	url(r'^$', 'get_latest_entries', name='blog'),
	# archives for blogs..
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'get_entries_for_day', name='entries_on_date'),
	# an entry on a specific date
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'get_post', name='blog_entry'),
	# entries with the specified tag
	url(r'^tags/(?P<tag>[\s\w\d\/\.]+)/$', 'get_entries_for_tag', name='entries_with_tag'),
	# search against entries
	url(r'^search/$', 'search', name='blog_search'),
)
