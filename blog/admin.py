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

from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from raptiye.blog.models import Entry

class FlatPageAdmin(FlatPageAdmin):
	class Media:
		js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce/textarea.js',)

class EntryAdmin(admin.ModelAdmin):
	model = Entry
	fieldsets = (
		(None, {
			"fields": ("title", "datetime", "content", "tags",
				("comments_enabled", "sticky", "published"), "language", "slug"),
		}),
	)
	date_hierarchy = "datetime"
	list_display = ("title", "get_datetime", "sticky", "published", "get_entry_url", "delete_entry")
	list_filter = ("published", "sticky")
	list_per_page = settings.ADMIN_LIST_PER_PAGE
	ordering = ("-datetime", "title")
	search_fields = ("title", "content", "tags__name")
	save_as = True
	radio_fields = {'language': admin.HORIZONTAL}
	prepopulated_fields = {"slug": ("title",)}
	
	class Media:
		js = ("js/tiny_mce/tiny_mce.js", "js/tiny_mce/textarea.js",)

admin.site.register(Entry, EntryAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)