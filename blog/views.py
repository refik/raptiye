#-*- encoding: utf-8 -*-

from pytz import timezone
from datetime import datetime
from django.conf import settings
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail, archive_day
from raptiye.blog.models import Entry
from raptiye.comments.views import create_captcha
from raptiye.extra.messages import *
from raptiye.extra.search import SearchAgainstEntries
from raptiye.tags.models import Tag

# creating a pytz info object for true utc time..
tz = timezone(settings.TIME_ZONE)

def search(request, lang='tr', template_name="blog/homepage.html"):
	"Search against all entries using the given keywords"

	if request.method == "GET" and request.GET.has_key("keywords"):
		keywords = request.GET["keywords"]
		
		if keywords.__len__() == 0:
			return get_latest_entries(request, MSG[lang]['SEARCH_NO_ITEM'], 
				lang='en', template_name='blog/homepage_en.html')
		
		keyword_list = keywords.split(" ")
		
		search = SearchAgainstEntries(keywords, lang)
		result = search.result()

		if result.__len__() == 0:
			return get_latest_entries(request, MSG[lang]['SEARCH_NO_ITEM'], 
				lang='en', template_name='blog/homepage_en.html')
		else:
			entry_list = {
				"queryset": result,
				"template_name": template_name,
				"template_object_name" : "entry",
				"paginate_by": settings.ENTRIES_PER_PAGE,
				"extra_context" : {
					"sticky" : MSG[lang]['SEARCH_SUCCESS'] % (keywords if keyword_list.__len__() == 1 else ", ".join(keyword_list), 
						MSG[lang]['SEARCH_KEYWORD'] if keyword_list.__len__() == 1 else MSG[lang]['SEARCH_KEYWORD_PLURAL'], result.__len__()),
				}
			}

			return object_list(request, **entry_list)
	else:
		return get_latest_entries(request, MSG[lang]['SEARCH_NO_ITEM'], 
			lang='en', template_name='blog/homepage_en.html')

def get_latest_entries_list(lang="tr"):
	return Entry.objects.filter(published=True, datetime__lte=datetime.now(tz), language=lang).order_by("-datetime")

def get_entries_for_day(request, year, month, day, lang='tr', template_name="blog/homepage.html"):
	"Displays all posts for a specific day"

	extra_context = {
		"sticky": MSG[lang]['ENTRIES_ON_DATE'] % (day, month, year),
	}

	entry = {
		"queryset" : get_latest_entries_list(lang),
		"template_name": template_name,
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

def get_post(request, year, month, day, slug, lang='tr', template_name="blog/detail.html"):
	"Displays a specific post"

	captcha = None
	extra_context = {}

	# don't create captcha if the user is not authenticated
	if request.user.is_authenticated():
		captcha = create_captcha()
		extra_context["captcha"] = captcha
	
	entry = {
		"queryset" : get_latest_entries_list(lang),
		"template_name": template_name,
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

def get_latest_entries(request, sticky="", lang="tr", template_name="blog/homepage.html"):
	entry_list = {
		"queryset": get_latest_entries_list(lang),
		"template_name": template_name,
		"template_object_name" : "entry",
		"paginate_by": settings.ENTRIES_PER_PAGE,
		"extra_context" : {
			"sticky" : sticky,
		}
	}

	return object_list(request, **entry_list)

def get_entries_for_tag(request, tag, lang='tr', template_name="blog/homepage.html"):
	# let's see if there's a tag with that name
	if Tag.objects.filter(name=tag).count() == 1:
		# found the tag, can continue
		t = Tag.objects.get(name=tag)
		entries = t.entries.filter(language=lang)
		entry_list = {
			"queryset": entries,
			"template_name": template_name,
			"template_object_name": "entry",
			"paginate_by": settings.ENTRIES_PER_PAGE,
			"extra_context" : {
				"sticky" : MSG[lang]['TAGS_SUCCESS'] % (tag, entries.count()),
			}
		}
		return object_list(request, **entry_list)
	return get_latest_entries(request, MSG[lang]['TAGS_ERROR'])