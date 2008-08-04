#-*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.blog.views',
	# english blog page
	(r'^$', 'get_latest_entries', {'lang': 'en', 'template_name': 'blog/homepage_en.html'}),
	
	# archives for blogs..
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 
		'get_entries_for_day', {'lang': 'en', 'template_name': 'blog/homepage_en.html'}, 
		name='entries_on_date'),
	
	# an English entry on a specific date
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 
		'get_post', {'lang': 'en', 'template_name': 'blog/detail_en.html'}, name='english_blog_entry'),
	
	# entries with the specified tag
	url(r'^tags/(?P<tag>[\s\w\d]+)/$', 'get_entries_for_tag', 
		{'lang': 'en', 'template_name': 'blog/homepage_en.html'}, name='english_entries_with_tag'),
	
	# search against entries
	url(r'^search/$', 'search', {'lang': 'en', 'template_name': 'blog/homepage_en.html'}, 
		name='english_blog_search'),
)