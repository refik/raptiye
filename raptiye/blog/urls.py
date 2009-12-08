#-*- encoding: utf-8 -*-
# raptiye
# Copyright (C)  Alper KANAT  <alperkanat@raptiye.org>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.blog.views',
	# main page of blog
	url(r'^$', 'get_latest_entries', name='blog'),
	# archives for blogs..
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'get_entries_for_day', name='entries_on_date'),
	# an entry on a specific date
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'get_post', name='blog_entry'),
	# entries with the specified tag
	url(r'^tags/(?P<slug>[\w\d-]+)/$', 'get_entries_for_tag', name='entries_with_tag'),
	# search against entries
	url(r'^search/$', 'search', name='blog_search'),
)
