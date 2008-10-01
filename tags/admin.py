from django.contrib import admin
from raptiye.tags.models import Tag

class TagAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag, TagAdmin)