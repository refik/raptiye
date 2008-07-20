#-*- encoding: utf-8 -*-

from pytz import timezone
from datetime import datetime
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def cut_text_by(value, arg):
	"Returns the text that's been truncated by arg"
	return value[:arg] + "..."

@register.filter
def is_text_larger_than(value, arg):
	"Returns true if larger, false otherwise"
	if value.__len__() > arg:
		return True
	else:
		return False

@register.simple_tag
def calculate_age():
	# creating a pytz info object for true utc time..
	tz = timezone(settings.TIME_ZONE)
	# my birth
	birth = datetime(1984, 05, 16, 10, 00, 00, 00, tz)
	return (datetime.now(tz) - birth).days/365

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
	# creating a pytz info object for true utc time..
	tz = timezone(settings.TIME_ZONE)
	now = datetime.now(tz)
	calendar = LocaleTextCalendar()
	return "%s" % calendar.formatmonthname(now.year, now.month, 0)

@register.simple_tag
def construct_calendar():
	from raptiye.blog.models import Entry
	from raptiye.extra.webcal import WebCalendar
	# creating a pytz info object for true utc time..
	tz = timezone(settings.TIME_ZONE)
	now = datetime.now(tz)
	wc = WebCalendar(now.year, now.month, now.day, Entry, "datetime")
	return wc.render("calendar_box", "/blog", u"bu tarihte yazılmış yazıları görmek için tıklayın..", "ulink")

@register.inclusion_tag('blog/pagination.html', takes_context=True)
def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page_numbers = range(max(1, context['page']-adjacent_pages), min(context['pages'], context['page']+adjacent_pages)+1)

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
    }
