# encoding: utf-8

from django.contrib import admin
from raptiye.links.models import *

class LinkCategoriesAdmin(admin.ModelAdmin):
	pass

class LinksAdmin(admin.ModelAdmin):
	pass

admin.site.register(LinkCategories, LinkCategoriesAdmin)
admin.site.register(Links, LinksAdmin)