from django.contrib import admin
from raptiye.polls.models import *

class ChoiceInline(admin.TabularInline):
	model = Choice
	max_num = 7
	extra = 2

class PollAdmin(admin.ModelAdmin):
	date_hierarchy = "datetime"
	list_display = ("question", "published", "get_results")
	list_filter = ("published",)
	search_fields = ["question",]
	inlines = [ChoiceInline,]

admin.site.register(Poll, PollAdmin)