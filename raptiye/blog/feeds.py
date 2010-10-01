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

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from tagging.models import Tag, TaggedItem

from raptiye.blog.functions import get_latest_entries

__all__ = ("RSS", "RSSLatestEntries", "RSSEntriesTaggedWith")

class RSS(Feed):
    title = settings.PROJECT_NAME
    title_template = "blog/feeds/latest_title.html"
    description = settings.PROJECT_SUBTITLE
    description_template = "blog/feeds/latest_description.html"

    def link(self):
        return reverse("index")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_url()

class RSSLatestEntries(RSS):
    def items(self):
        return get_latest_entries()[:settings.RSS_LIMIT]

class RSSEntriesTaggedWith(RSS):
    """
    Renders the latest N entries tagged with a given tag.

    Sample URL: /feeds/entries_tagged_with/tag/

    """

    def get_object(self, request, tag):
        return get_object_or_404(Tag, name=tag)

    def items(self, item):
        return TaggedItem.objects.get_by_model(get_latest_entries(), item)[:settings.RSS_LIMIT]
