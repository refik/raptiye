# raptiye
# Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # homepage view
    url(r'^$', 'raptiye.blog.views.index', name="index"),

    # file browser
    (r'^admin/filebrowser/', include('filebrowser.urls')),

    # admin page
    (r'^admin/', include(admin.site.urls)),

    # admin tools
    url(r'^admin_tools/', include('admin_tools.urls')),

    # blog page
    (r'^blog/', include('raptiye.blog.urls')),

    # grappelli
    (r'^grappelli/', include('raptiye.grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
