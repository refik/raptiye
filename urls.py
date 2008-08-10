from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from raptiye.blog.feeds import LatestEntries

admin.autodiscover()

feeds = {
	'latest': LatestEntries,
}

urlpatterns = patterns('',
	# main page
	(r'^$', 'raptiye.frontpage.views.index'),

	# admin page
	url(r'^admin/(.*)', admin.site.root, name='admin_page'),

	# blog page
	(r'^blog/', include('raptiye.blog.urls')),

	# comment related stuff
	(r'^comment/', include('raptiye.comments.urls')),

	# feed related stuff
	url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name='rss_feed'),

	# users related stuff like login, register
	(r'^users/', include('raptiye.users.urls')),
)

# should be deleted in the production phase
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
