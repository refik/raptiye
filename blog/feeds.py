#-*- encoding: utf-8 -*-

from datetime import datetime
import locale
from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from raptiye.blog.views import get_latest_entries_list
from raptiye.frontpage.models import FrontPage
from raptiye.tags.models import Tag

class RSS(Feed):
	language = u"en"
	title_template = "feeds/latest_title.html"
	description_template = "feeds/latest_description.html"
	
	def title(self):
		fp = FrontPage.objects.get(pk=1)
		return fp.title
	
	def description(self):
		fp = FrontPage.objects.get(pk=1)
		return fp.subtitle
	
	def link(self):
		fp = FrontPage.objects.get(pk=1)
		return fp.links.get(title="Günlük").url
	
	def item_link(self, item):
		return item.get_full_url()
	
	def item_pubdate(self, item):
		# setting locale
		locale.setlocale(locale.LC_ALL, settings.LOCALES["en"])
		return item.datetime

class RSSLatestEntries(RSS):
	def items(self):
		fp = FrontPage.objects.get(pk=1)
		return get_latest_entries_list()[:fp.rss_limit]

class AtomLatestEntries(RSSLatestEntries):
	feed_type = Atom1Feed
	subtitle = RSS.description

class RSSEntriesWithTag(RSS):
	# /feeds/entries_tagged_with/tag_name_here
	
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
			
		return Tag.objects.get(name=bits[0])
	
	def items(self, obj):
		fp = FrontPage.objects.get(pk=1)
		return obj.entries.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime")[:fp.rss_limit]