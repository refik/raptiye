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

from django.core.exceptions import ObjectDoesNotExist

from raptiye.blog.feeds import RSS
from raptiye.tags.models import Tag

class RSSEntriesWithTag(RSS):
    # /feeds/entries_tagged_with/tag_slug_here

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist

        return Tag.objects.get(slug=bits[0])

    def items(self, obj):
        return obj.entries.filter(
                published=True,
                datetime__lte=datetime.now()
            ).order_by("-datetime")[:settings.RSS_LIMIT]

