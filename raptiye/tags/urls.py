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

from django.conf.urls.defaults import *

from raptiye.tags.feeds import RSSEntriesTaggedWith

urlpatterns = patterns('raptiye.tags.views',
    url(r'^(?P<tag>[^/]+)/$', 'entries_tagged_with', name='entries_tagged_with'),
)

# feeds
urlpatterns += patterns('',
    url(r'^feeds/(?P<tag>[^/]+)/$', RSSEntriesTaggedWith(), name="rss_entries_tagged_with"),
)
