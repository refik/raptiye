from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from raptiye.blog.models import Entry

class Comments(models.Model):
	entry = models.ForeignKey(Entry, verbose_name=u"Entry")
	author = models.ForeignKey(User, verbose_name=u"Author")
	datetime = models.DateTimeField(auto_now_add=True)
	content = models.TextField(u"Comment")
	published = models.BooleanField(u"Published", default=False)
	notification = models.BooleanField(u"Notification", default=False)

	def __unicode__(self):
		return "Comment for '" + self.entry.title + "' by " + self.author.username

	def get_entry_name(self):
		return self.entry.title

	get_entry_name.short_description = "Entry Title"

	def get_datetime(self):
		return self.datetime.strftime("%d.%m.%Y @ %H:%M")

	get_datetime.short_description = "Comment Written On"

	def get_author_info(self):
		return self.author.username + " - <a href='mailto: " + self.author.email + "'>" + self.author.email + "</a>"

	get_author_info.short_description = "User Info"
	get_author_info.allow_tags = True

	class Meta:
		get_latest_by = "datetime"
		ordering = ["-datetime"]
		verbose_name = "Comment"
		verbose_name_plural = "Comments"
