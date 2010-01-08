from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.contrib.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)

