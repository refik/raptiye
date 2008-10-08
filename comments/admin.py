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
from raptiye.comments.models import Comments

class CommentsAdmin(admin.ModelAdmin):
	model = Comments
	date_hierarchy = "datetime"
	list_display = ("get_entry_name", "get_author_info", "get_author_web_site", "get_datetime", "published", "notification", "get_entry_url")
	list_filter = ("published", "notification")
	list_per_page = settings.ADMIN_LIST_PER_PAGE
	ordering = ("-datetime",)
	search_fields = ("entry__title", "author__username", "content")
	
	def save_model(self, request, obj, form, change):
		# if the comment is allowed to be published, then we need
		# to notify the other users that want to be notified for a 
		# particular blog post..
		obj.save()
		
		if obj.published:
			from raptiye.extra.mail import send_comment_notification
			send_comment_notification(obj.entry, obj.author)

admin.site.register(Comments, CommentsAdmin)