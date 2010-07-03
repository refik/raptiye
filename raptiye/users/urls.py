# coding: utf-8
# 
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
from django.core.urlresolvers import reverse

from raptiye.extra.utils import reverse as lazy_reverse

urlpatterns = patterns('raptiye.users.views',
    url(r'^reset/password/being/confirmed/$', 'being_confirmed', name='being_confirmed'),
)

# builtin views with custom parameters
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {
        'template_name': 'login.html'
    }, name='login'),
    url(r'^logout/$', 'logout', {
        'next_page': reverse('blog:index')
    }, name='logout'),
    url(r'^reset/password/$', 'password_reset', {
        'template_name': 'password_reset_form.html',
        'email_template_name': 'password_reset_email.html',
        'post_reset_redirect': lazy_reverse("users:being_confirmed")
    }, name='password_reset'),
    url(r'^reset/password/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', {
        'template_name': 'password_reset_confirm.html',
        'post_reset_redirect': reverse('blog:index')
    }, name='password_reset_confirm'),
)
