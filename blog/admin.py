from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from raptiye.blog.models import Entry

class FlatPageAdmin(FlatPageAdmin):
	class Media:
		js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce/textarea.js',)

class EntryAdmin(admin.ModelAdmin):
	model = Entry
	fieldsets = (
		(None, {
			"fields": ("title", "datetime", "content", "tags",
				("comments_enabled", "sticky", "published"), "language", "slug"),
		}),
	)
	date_hierarchy = "datetime"
	list_display = ("title", "get_datetime", "sticky", "published", "get_entry_url", "delete_entry")
	list_filter = ("published", "sticky")
	list_per_page = settings.ADMIN_LIST_PER_PAGE
	ordering = ("-datetime", "title")
	search_fields = ("title", "content", "tags__name")
	save_as = True
	radio_fields = {'language': admin.HORIZONTAL}
	prepopulated_fields = {"slug": ("title",)}
	
	class Media:
		js = ("js/tiny_mce/tiny_mce.js", "js/tiny_mce/textarea.js",)

admin.site.register(Entry, EntryAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)