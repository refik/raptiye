#-*- encoding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from raptiye.blog.views import get_latest_entries_list
from raptiye.frontpage.models import FrontPage

class RSSLatestEntries(Feed):
	fp = FrontPage.objects.get(pk=1)
	title = fp.title
	link = '/blog/'
	description = fp.subtitle
	language = u"en"
	
	def item_link(self, item):
		return item.get_full_url()
	
	def item_pubdate(self, item):
		return item.datetime
	
	def items(self):
		fp = FrontPage.objects.get(pk=1)
		return get_latest_entries_list()[:fp.rss_limit]