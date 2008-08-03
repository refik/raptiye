from django.conf.urls.defaults import *

urlpatterns = patterns('',
	# turkish homepage
	url(r'^$', 'raptiye.frontpage.views.index', name='turkish_homepage'),

	# blog page
	(r'^blog/', include('raptiye.blog.urls')),

	# users related stuff like login, register
	(r'^users/', include('raptiye.users.urls')),
)