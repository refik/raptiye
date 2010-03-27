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

from raptiye.blog.models import *

class EntryAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    date_hierarchy = "datetime"
    fieldsets = (
        (None, {
            "fields": ("title", "datetime", "content",
                ("comments_enabled", "sticky", "published"), "language", "slug"),
        }),
    )
    list_display = ("title", "datetime", "sticky", "published")
    list_filter = ("published", "sticky")
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    model = Entry
    ordering = ("-datetime", "title")
    prepopulated_fields = {"slug": ("title",)}
    radio_fields = {'language': admin.HORIZONTAL}
    save_as = True
    save_on_top = True
    search_fields = ("title", "content")

    class Media:
        # js = ("js/fckeditor/fckeditor.js", "js/fckeditor_inclusion.js")
        pass

admin.site.register(Entry, EntryAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url', 'window')
    list_filter = ('window',)
    search_fields = ['title', 'description']

admin.site.register(Link, LinkAdmin)
