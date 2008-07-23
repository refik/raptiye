from django.contrib import admin
from raptiye.tags.models import Tag

class TagAdmin(admin.ModelAdmin):
	pass

admin.site.register(Tag, TagAdmin)
