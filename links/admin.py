# encoding: utf-8

from django.contrib import admin
from raptiye.links.models import *

class LinkCategoriesAdmin(admin.ModelAdmin):
	list_display = ('title', 'show_image', 'level')
	search_fields = ['title']

class LinksAdmin(admin.ModelAdmin):
	# TODO: add tags here..
	list_display = ('title', 'description', 'go_to_url', 'category', 'window')
	list_filter = ('category', 'window')
	search_fields = ['title', 'category__title', 'description', 'tags__name']

admin.site.register(LinkCategories, LinkCategoriesAdmin)
admin.site.register(Links, LinksAdmin)