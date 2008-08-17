#-*- encoding: utf-8 -*-

from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail, archive_day
from raptiye.blog.models import Entry
from raptiye.comments.views import create_captcha
from raptiye.extra.messages import TAGS_SUCCESS, TAGS_ERROR, SEARCH_FAILED, SEARCH_NO_ITEM
from raptiye.extra.search import SearchAgainstEntries
from raptiye.tags.models import Tag

def search(request, template="blog/homepage.html"):
	"Search against all entries using the given keywords"

	if request.method == "GET" and request.GET.has_key("keywords"):
		keywords = request.GET["keywords"]
		keyword_list = keywords.split(" ")

		search = SearchAgainstEntries(keywords)
		result = search.result()

		if result.__len__() == 0:
			return get_latest_entries(request, SEARCH_NO_ITEM)
		else:
			entry_list = {
				"queryset": result,
				"template_name": "blog/homepage.html",
				"template_object_name" : "entry",
				"paginate_by": settings.ENTRIES_PER_PAGE,
				"extra_context" : {
					"sticky" : u"<strong><i>%s</i></strong> %s içeren yazılar (%d) görüntüleniyor.." % (keywords if keyword_list.__len__() == 1 else ", ".join(keyword_list), 
						"kelimesini" if keyword_list.__len__() == 1 else "kelimelerini", result.__len__()),
				}
			}

			return object_list(request, **entry_list)
	else:
		return get_latest_entries(request, SEARCH_FAILED)

def get_latest_entries_list():
	return Entry.objects.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime")

def get_entries_for_day(request, year, month, day):
	"Displays all posts for a specific day"

	extra_context = {
		"sticky": u"%s.%s.%s tarihinde yazılmış yazılar görüntüleniyor.." % (day, month, year),
	}

	entry = {
		"queryset" : Entry.objects.all(),
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

	captcha = None
	extra_context = {}

	# don't create captcha if the user is not authenticated
	if request.user.is_authenticated():
		captcha = create_captcha()
		extra_context["captcha"] = captcha
	
	entry = {
		"queryset" : Entry.objects.all(),
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

def get_latest_entries(request, sticky=""):
	entry_list = {
		"queryset": get_latest_entries_list(),
		"template_name": "blog/homepage.html",
		"template_object_name" : "entry",
		"paginate_by": settings.ENTRIES_PER_PAGE,
		"extra_context" : {
			"sticky" : sticky,
		}
	}

	return object_list(request, **entry_list)

def get_entries_for_tag(request, tag):
	# let's see if there's a tag with that name
	if Tag.objects.filter(name=tag).count() == 1:
		# found the tag, can continue
		t = Tag.objects.get(name=tag)
		entry_list = {
			"queryset": t.entries.all(),
			"template_name": "blog/homepage.html",
			"template_object_name": "entry",
			"paginate_by": settings.ENTRIES_PER_PAGE,
			"extra_context" : {
				"sticky" : TAGS_SUCCESS % (tag, t.entries.count()),
			}
		}
		return object_list(request, **entry_list)
	return get_latest_entries(request, TAGS_ERROR % (u"etiket hatalı mı ne?", u"aradığınız etikete şu anda ulaşılamıyor.. etiket kapalı ya da kapsama alanı dışında.."))
