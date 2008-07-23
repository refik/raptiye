from django.contrib import admin
from raptiye.comments.models import Comments

class CommentsAdmin(admin.ModelAdmin):
	model = Comments
	date_hierarchy = "datetime"
	list_display = ("get_entry_name", "get_author_info", "get_datetime", "published", "notification",)
	list_filter = ("published",)
	list_per_page = settings.ADMIN_LIST_PER_PAGE
	ordering = ("-datetime")
	search_fields = ("entry__title", "author__username", "content")

admin.site.register(Comments, CommentsAdmin)
