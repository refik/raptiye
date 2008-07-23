from django.contrib import admin
from raptiye.frontpage.models import FrontPage

class FrontPageAdmin(admin.ModelAdmin):
	model = FrontPage
	radio_fields = {'language', admin.HORIZONTAL}

admin.site.register(FrontPage, FrontPageAdmin)
