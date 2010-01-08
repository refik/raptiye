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

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from raptiye.blog.functions import get_latest_entries

def index(request, template_name="blog/homepage.html"):
    dict = {
        "queryset": get_latest_entries(),
        "template_name": template_name,
        "paginate_by": settings.ENTRIES_PER_PAGE,
        "page": request.GET.get("page", 1),
        "template_object_name": "entry",
    }

    return object_list(request, **dict)

