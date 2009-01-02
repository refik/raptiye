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

from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('raptiye.users.views',
	# openid complete page
	url(r'^openid/complete/$', 'openid_complete', name="openid_complete"),
	# register page
	url(r'^register/$', 'register', name='registration'),
	# login page
	url(r'^login/$', 'user_login', name='login_page'),
	# logout page
	url(r'^logout/$', 'user_logout', name='logout_page'),
	# forgotten password page
	url(r'^forgotten_password/$', 'forgotten_password', name='forgotten_password'),
	# activation page
	url(r'^(?P<username>[\w\d]+)/activate/(?P<key>[\w\d]+)/$', 'activation', name='activation_page'),
	# gravatar request
	url(r'^(?P<username>[\w\d]+)/profile/gravatar/$', 'gravatar', name='gravatar_request'),
	# profile page
	url(r'^(?P<username>[\w\d]+)/profile/$', 'profile', name='profile_page'),
	# profile page notification removal
	url(r'^(?P<username>[\w\d]+)/profile/notification/remove/$', 'notification_remove', name='notification_removal'),
)