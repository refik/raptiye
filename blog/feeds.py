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
		# FIXME: title=günlük is stupid! change it!
		return fp.links.get(title="günlük").url
	
	def item_link(self, item):
		return item.get_full_url()
	
	def item_pubdate(self, item):
		# setting locale
		locale.setlocale(locale.LC_ALL, settings.LOCALES["en"])
		return item.datetime

class RSSLatestEntries(RSS):
	def items(self):
		fp = FrontPage.objects.get(pk=1)
		return get_latest_entries_list(show_sticky=True)[:fp.rss_limit]

class AtomLatestEntries(RSSLatestEntries):
	feed_type = Atom1Feed
	subtitle = RSS.description

class RSSEntriesWithTag(RSS):
	# /feeds/entries_tagged_with/tag_slug_here
	
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
			
		return Tag.objects.get(slug=bits[0])
	
	def items(self, obj):
		fp = FrontPage.objects.get(pk=1)
		return obj.entries.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime")[:fp.rss_limit]