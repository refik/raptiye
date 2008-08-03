from django.conf.urls.defaults import *

urlpatterns = patterns('',	
	# main page in English
	url(r'^$', 'raptiye.frontpage.views.index', {'lang': 'en', 'template_name': 'frontpage/homepage_en.html'}, name='english_homepage'),
	
	# english blog page
	(r'^blog/', 'raptiye.blog.views.get_latest_entries', {'lang': 'en', 'template_name': 'blog/homepage_en.html'}),
)