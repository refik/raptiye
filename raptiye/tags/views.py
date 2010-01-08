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
from django.views.generic.list_detail import object_list

from raptiye.blog.views import get_latest_entries
from raptiye.extra import messages
from raptiye.tags.models import Tags

def get_entries_for_tag(request, slug):
    # let's see if there's a tag with that name
    if Tags.objects.filter(slug=slug).exists():
        # found the tag, can continue
        t = Tags.objects.get(slug=slug)
        
        entry_list = {
            "queryset": t.entries.filter(published=True, datetime__lte=datetime.now()).order_by("-datetime"),
            "template_name": "blog/homepage.html",
            "template_object_name": "entry",
            "paginate_by": settings.ENTRIES_PER_PAGE,
            "extra_context" : {
                "messages" : (messages.TAGS_SUCCESS % (t.name, t.entries.count()),),
            }
        }

        return object_list(request, **entry_list)

    # can't find the tag.. leaving a message for the visitor
    messages.set_user_message(request, messages.TAGS_ERROR)

    return get_latest_entries(request)

