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
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.date_based import object_detail
from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from raptiye.blog.functions import *
from raptiye.blog.models import Entry

def index(request):
    return redirect("blog", permanent=True)

def show_preview(request, template_name="preview.html"):
    if request.is_ajax():
        return render_to_response(template_name, context_instance=RequestContext(request))
    raise Http404

def blog(request, template_name="homepage.html"):
    params = {
        "queryset": get_latest_entries(),
        "template_name": template_name,
        "paginate_by": settings.ENTRIES_PER_PAGE,
        "page": request.GET.get("page", 1),
        "template_object_name": "entry",
    }

    return object_list(request, **params)

def show_post(request, year, month, day, slug, template_name="detail.html"):
    params = {
        "year": year,
        "month": month,
        "day": day,
        "queryset": get_latest_entries(),
        "date_field": "datetime",
        "slug": slug,
        "month_format": "%m",
        "template_name": template_name,
        "template_object_name": "entry",
        "allow_future": True
    }
    
    return object_detail(request, **params)

def search(request, template_name="search.html"):
    "Search against all entries using the given keywords"

    keywords = request.GET.get("keywords", "")
    result = search_against_entries(keywords)

    params = {
        "queryset": result,
        "template_name": template_name,
        "template_object_name" : "entry",
        "paginate_by": settings.ENTRIES_PER_PAGE,
        "extra_context": {
            "keywords": keywords
        }
    }

    return object_list(request, **params)

def entries_tagged_with(request, tag, template_name="tags/entries_tagged_with.html"):
    params = {
        "queryset_or_model": get_latest_entries(),
        "tag": tag,
        "template_name": template_name,
        "paginate_by": settings.ENTRIES_PER_PAGE,
        "page": request.GET.get("page", 1),
        "template_object_name": "entry",
        # FIXME: the following line results as an AttributeError due to bug #179
        # (http://code.google.com/p/django-tagging/issues/detail?id=179)
        # "related_tags": True,
    }

    return tagged_object_list(request, **params)
