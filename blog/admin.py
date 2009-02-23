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
from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from raptiye.blog.models import Entry

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
		js = ("js/fckeditor/fckeditor.js", "js/fckeditor_inclusion.js")
	
	def save_model(self, request, obj, form, change):
		obj.save()
		
		if settings.POST_TO_TWITTER and obj.published:
			from raptiye.contrib import twitter
			from raptiye.extra.tinyurl import shorten_url
			
			try:
				api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD, input_encoding="utf8")
				api.PostUpdate(u"%s (%s)" % (obj.title, shorten_url(obj.get_full_url())))
			except:
				pass

admin.site.register(Entry, EntryAdmin)

class FlatPageAdmin(FlatPageAdminOld):
	class Media:
		js = ("js/fckeditor/fckeditor.js", "js/fckeditor_inclusion.js")

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)