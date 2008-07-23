from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	# main page
	(r'^$', 'raptiye.frontpage.views.index'),

	# admin page
	(r'^admin/(.*)', admin.site.root),

	# blog page
	(r'^blog/', include('raptiye.blog.urls')),

	# comment related stuff
	(r'^comment/', include('raptiye.comments.urls')),

	# users related stuff like login, register
	(r'^users/', include('raptiye.users.urls')),
)

# should be deleted in the production phase
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)

