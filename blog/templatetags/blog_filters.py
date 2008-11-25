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

from datetime import datetime
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def calculate_age():
	# my birth
	birth = datetime(1984, 05, 16, 10, 00, 00, 00)
	return (datetime.now() - birth).days/365

@register.tag
def construct_tag_cloud(parser, token):
	from raptiye.extra.tag_cloud import TagCloud
	tgc = TagCloud()
	return TagCloudNode(tgc.get_tag_cloud())

class TagCloudNode(template.Node):
	def __init__(self, cloud):
		self.cloud = cloud
	
	def render(self, context):
		context["tagcloud"] = self.cloud
		return ""

@register.simple_tag
def get_month_and_year():
	from calendar import LocaleTextCalendar
	now = datetime.now()
	calendar = LocaleTextCalendar(0, settings.LOCALES['tr'])
	month_and_year = u"%s" % calendar.formatmonthname(now.year, now.month, 0)
	return month_and_year.lower()

@register.simple_tag
def construct_calendar():
	from raptiye.blog.models import Entry
	from raptiye.extra.webcal import WebCalendar
	from raptiye.extra.messages import ENTRIES_ON_DATE
	now = datetime.now()
	wc = WebCalendar(now.year, now.month, now.day, Entry.objects.exclude(sticky=True), "datetime", settings.LOCALES['tr'])
	return wc.render("calendar_box", "/blog", ENTRIES_ON_DATE, "ulink")

@register.inclusion_tag('blog/pagination.html', takes_context=True)
def paginator(context, adjacent_pages=2):
	"""
	To be used in conjunction with the object_list generic view.
	
	Adds pagination context variables for use in displaying first, adjacent and
	last page links in addition to those created by the object_list generic
	view.
	
	"""
	page_numbers = range(max(1, context['page']-adjacent_pages), min(context['pages'], context['page']+adjacent_pages)+1)
	
	params = context["request"].GET.copy()
	
	if params.__contains__("page"):
		del(params["page"])
	
	return {
		'page': context['page'],
		'pages': context['pages'],
		'page_numbers': page_numbers,
		'next': context['next'],
		'previous': context['previous'],
		'has_next': context['has_next'],
		'has_previous': context['has_previous'],
		'show_first': 1 not in page_numbers,
		'show_last': context['pages'] not in page_numbers,
		"query_string": params.urlencode(),
	}

@register.inclusion_tag('blog/links.html')
def links():
	'Adds all link categories and their links to the context..'
	
	from raptiye.links.models import LinkCategories
	
	return {
		'link_category': LinkCategories.objects.all(),
	}

@register.inclusion_tag("blog/sticky.html")
def sticky():
	"""
	Grabs the latest sticky post and show it.. Since raptiye is not a forum
	app, I don't think there might be more than 1 sticky posts at a time and
	therefore not implementing it.
	
	Sticky posts are excluded from the following:
	
	* RSS feeds
	* Search results
	* Blog entry listings
	
	If you want to publish a blog entry after you made it sticky, then simple 
	remove its sticky flag..
	"""
	from raptiye.blog.models import Entry
	
	sticky_flag = True if Entry.objects.filter(sticky=True).count() == 1 else False
	latest_sticky_post = Entry.objects.filter(sticky=True).latest() if sticky_flag else None
	
	return {
		"sticky_flag": sticky_flag,
		"sticky_post": latest_sticky_post,
	}

@register.filter
def emotions(entry):
	from django.contrib.sites.models import Site
	
	site = Site.objects.get_current()
	
	icons = {
		":)": "/media/images/smiley/face-smile.png",
		":|": "/media/images/smiley/face-plain.png",
		":(": "/media/images/smiley/face-sad.png",
		":D": "/media/images/smiley/face-grin.png",
		";-)": "/media/images/smiley/face-wink.png",
	}
	
	for smiley, src in icons.iteritems():
		entry = entry.replace(smiley, " <img src='http://%s%s' align='absmiddle'> " % (site.domain, src))
	
	return entry

@register.inclusion_tag("blog/twitter.html")
def twitter():
	"""
	Gets the latest Twitter status updates of the blog author
	using the credentials in settings.py
	"""
	from raptiye.contrib import twitter
	
	if settings.TWITTER_USERNAME != "" and settings.TWITTER_PASSWORD != "":
		try:
			api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
			latest_updates_of_user = [status.GetText() for status in api.GetUserTimeline()]
			return {"latest_updates": latest_updates_of_user[:settings.TWITTER_LIMIT]}
		except:
			# generally this is the case that we get "connection timed out"
			pass
	return {"latest_updates": None}

@register.filter
def entrycutter(entry):
	if len(entry.split()) > 150:
		return True
	return False