#-*- coding: utf-8 -*-
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

from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail, archive_day

from raptiye.blog.models import Entry
from raptiye.comments.views import create_captcha
from raptiye.extra import messages
from raptiye.extra.search import SearchAgainstEntries
from raptiye.tags.models import Tag

# FIXME: remove hardcoded strings

def search(request, template="blog/homepage.html"):
	"Search against all entries using the given keywords"

	if request.method == "GET" and request.GET.has_key("keywords"):
		keywords = request.GET["keywords"]
		keyword_list = keywords.split(" ")

		search = SearchAgainstEntries(keywords)
		result = search.result()

		if result.__len__() == 0:
			messages.set_user_message(request, messages.SEARCH_NO_ITEM)
			return get_latest_entries(request)
		else:
			entry_list = {
				"queryset": result,
				"template_name": "blog/homepage.html",
				"template_object_name" : "entry",
				"paginate_by": settings.ENTRIES_PER_PAGE,
				"extra_context" : {
					"messages" : (messages.SEARCH_BODY % (keywords if keyword_list.__len__() == 1 else ", ".join(keyword_list), 
						messages.SEARCH_WORD if keyword_list.__len__() == 1 else messages.SEARCH_WORD_PLURAL, result.__len__()),),
				}
			}

			return object_list(request, **entry_list)
	else:
		messages.set_user_message(request, messages.SEARCH_FAILED)
		return get_latest_entries(request)

def get_latest_entries_list():
	return Entry.objects.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime")

def get_entries_for_day(request, year, month, day):
	"Displays all posts for a specific day"

	extra_context = {
		"messages": (messages.ENTRIES_FOR_DAY % (day, month, year),),
	}

	entry = {
		"queryset" : Entry.objects.filter(published=True, datetime__lte=datetime.now()),
		"template_name": "blog/homepage.html",
		"template_object_name": "entry",
		"year": year,
		"month": month,
		"day": day,
		"date_field": "datetime",
		"month_format": "%m",
		"day_format": "%d",
		"allow_future": True,
		"extra_context": extra_context,
	}
	return archive_day(request, **entry)

def get_post(request, year, month, day, slug):
	"Displays a specific post"
	
	from raptiye.comments.forms import CommentForm
	
	captcha = None
	extra_context = {
		"allow_anonymous_comments": settings.ALLOW_ANONYMOUS_COMMENTS and not request.user.is_authenticated(),
		"form": CommentForm(),
	}

	# don't create captcha if the user is not authenticated
	if settings.ALLOW_ANONYMOUS_COMMENTS or request.user.is_authenticated():
		captcha = create_captcha()
		extra_context["captcha"] = captcha
	
	entry = {
		"queryset" : Entry.objects.filter(published=True, datetime__lte=datetime.now()),
		"template_name": "blog/detail.html",
		"template_object_name": "entry",
		"year": year,
		"month": month,
		"day": day,
		"slug": slug,
		"date_field": "datetime",
		"slug_field": "slug",
		"month_format": "%m",
		"day_format": "%d",
		"allow_future": True,
		"extra_context": extra_context,
	}
	return object_detail(request, **entry)

def get_latest_entries(request):
	entry_list = {
		"queryset": get_latest_entries_list().exclude(sticky=True),
		"template_name": "blog/homepage.html",
		"template_object_name" : "entry",
		"paginate_by": settings.ENTRIES_PER_PAGE,
	}
	return object_list(request, **entry_list)

def get_entries_for_tag(request, slug):
	# let's see if there's a tag with that name
	if Tag.objects.filter(slug=slug).count() == 1:
		# found the tag, can continue
		t = Tag.objects.get(slug=slug)
		entry_list = {
			"queryset": t.entries.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime"),
			"template_name": "blog/homepage.html",
			"template_object_name": "entry",
			"paginate_by": settings.ENTRIES_PER_PAGE,
			"extra_context" : {
				"messages" : (messages.TAGS_SUCCESS % (t.name, t.entries.count()),),
			}
		}
		return object_list(request, **entry_list)
	
	# can't find the tag.. leaving a message for the visitor
	messages.set_user_message(request, messages.TAGS_ERROR)
	
	return get_latest_entries(request)

