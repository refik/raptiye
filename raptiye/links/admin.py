# encoding: utf-8
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

from django.contrib import admin
from raptiye.links.models import *

class LinkCategoriesAdmin(admin.ModelAdmin):
	list_display = ('title', 'show_image', 'level')
	search_fields = ['title']

class LinksAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'go_to_url', 'get_linked_category', 'get_tags_for_link', 'window')
	list_filter = ('category', 'window')
	search_fields = ['title', 'category__title', 'description', 'tags__name']

admin.site.register(LinkCategories, LinkCategoriesAdmin)
admin.site.register(Links, LinksAdmin)