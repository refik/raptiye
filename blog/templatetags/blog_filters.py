#-*- encoding: utf-8 -*-

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
	return u"%s" % calendar.formatmonthname(now.year, now.month, 0)

@register.simple_tag
def construct_calendar():
	from raptiye.blog.models import Entry
	from raptiye.extra.webcal import WebCalendar
	from raptiye.extra.messages import ENTRIES_ON_DATE
	now = datetime.now()
	wc = WebCalendar(now.year, now.month, now.day, Entry, "datetime", settings.LOCALES['tr'])
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