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

from django.shortcuts import render_to_response
from django.template import RequestContext
from raptiye.blog.views import get_latest_entries_list
from raptiye.frontpage.models import FrontPage

def index(request, template_name='frontpage/homepage.html'):
	try:
		fp = FrontPage.objects.get(pk=1)
		# getting latest blog entries (with limit in settings)
		entries = get_latest_entries_list()
		# put them together into a dict
		dict = {
			'entries': entries[:fp.rss_limit]
		}
		# now we have everything.. let's show it..
		return render_to_response(template_name, dict, context_instance=RequestContext(request))
	except FrontPage.DoesNotExist:
		return render_to_response("frontpage/initial.html")