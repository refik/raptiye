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
from raptiye.frontpage.models import FrontPage
from raptiye.frontpage.models import Links

class LinksInline(admin.TabularInline):
	model = Links
	max_num = 5
	extra = 2

class FrontPageAdmin(admin.ModelAdmin):
	model = FrontPage
	radio_fields = {'language': admin.HORIZONTAL}
	inlines = [
		LinksInline,
	]

admin.site.register(FrontPage, FrontPageAdmin)
