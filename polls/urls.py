from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.polls.views',
		# submitting poll answer
	url(r'^submit/$', "polls", name="polls"),
)