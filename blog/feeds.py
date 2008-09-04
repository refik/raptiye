#-*- encoding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from raptiye.blog.views import get_latest_entries_list
from raptiye.frontpage.models import FrontPage
from raptiye.tags.models import Tag

class RSS(Feed):
	fp = FrontPage.objects.get(pk=1)
	title = fp.title
	link = '/blog/'
	description = fp.subtitle
	language = u"en"
	title_template = "feeds/latest_title.html"
	description_template = "feeds/latest_description.html"
	
	def item_link(self, item):
		return item.get_full_url()
	
	def item_pubdate(self, item):
		return item.datetime

class RSSLatestEntries(RSS):
	def items(self):
		fp = FrontPage.objects.get(pk=1)
		return get_latest_entries_list()[:fp.rss_limit]

class AtomLatestEntries(RSSLatestEntries):
	feed_type = Atom1Feed
	subtitle = RSS.description