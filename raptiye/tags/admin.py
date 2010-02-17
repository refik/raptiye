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
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from raptiye.blog.admin import EntryAdmin
from raptiye.blog.models import Entry
from raptiye.tags.models import Tag, TaggedEntry

class TaggedEntryAdmin(EntryAdmin):
    model = TaggedEntry
    fieldsets = (
        (None, {
            "fields": ("title", "datetime", "content", "tags",
                ("comments_enabled", "sticky", "published"), "language", "slug"),
        }),
    )
    filter_horizontal = ("tags",)

admin.site.unregister(Entry)
admin.site.register(TaggedEntry, TaggedEntryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "url_for_tag")
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    search_fields = ("name",)
    
    def url_for_tag(self, obj):
        """
        Returns the reverse URL for tag
        
        """
        
        return "<a href='%s' target='_blank'>%s</a>" % (reverse("entries_tagged_with", args=[obj.slug]), obj.name)
    
    url_for_tag.short_description = _(u"URL")
    url_for_tag.allow_tags = True

admin.site.register(Tag, TagAdmin)
