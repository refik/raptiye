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
