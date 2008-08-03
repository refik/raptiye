from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from raptiye.blog.feeds import LatestEntries

admin.autodiscover()

feeds = {
	'latest': LatestEntries,
}

urlpatterns = patterns('',
	# main page in Turkish
	(r'^tr/', include('raptiye.tr-urls')),

	# main page in English
	(r'^en/', include('raptiye.en-urls')),

	# comment related stuff
	(r'^comment/', include('raptiye.comments.urls')),

	# admin page
	url(r'^admin/(.*)', admin.site.root, name='admin_page'),

	# feed related stuff
	url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'rss_feed'),
)

# should be deleted in the production phase
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
