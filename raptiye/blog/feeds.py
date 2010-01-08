# coding: utf-8
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
# 

import locale
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from raptiye.blog.functions import get_latest_entries

class RSS(Feed):
    language = u"en"
    title_template = "blog/feeds/latest_title.html"
    description_template = "blog/feeds/latest_description.html"

    def title(self):
        return settings.PROJECT_NAME

    def description(self):
        return settings.PROJECT_SUBTITLE

    def link(self):
        site = Site.objects.get_current()
        return "http://%s" % site.domain

    def item_link(self, item):
        # TODO: place the correct link here!
        return reverse("blog")

    def item_pubdate(self, item):
        # setting locale
        locale.setlocale(locale.LC_ALL, settings.LOCALES["en"])
        return item.datetime

class RSSLatestEntries(RSS):
    def items(self):
        return get_latest_entries()[:settings.RSS_LIMIT]

class AtomLatestEntries(RSSLatestEntries):
    feed_type = Atom1Feed
    subtitle = RSS.description

