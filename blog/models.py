#-*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from raptiye.tags.models import Tag

class Entry(models.Model):
	"""
	Entry Class

	This is the class we hold every post for the blog. It
	can be either in Turkish or English due to the choices
	in settings.
	"""

	title = models.CharField(u"Title", help_text="Required", max_length=80)
	datetime = models.DateTimeField(u"Publish On", help_text="Required")
	content = models.TextField(u"Content", help_text="Required.. HTML Allowed..")
	tags = models.ManyToManyField(Tag, verbose_name="tags", related_name="entries")
	sticky = models.BooleanField(u"Sticky", default=False)
	language = models.CharField(u"Language", choices=settings.LANGUAGES, default="tr", max_length=2)
	published = models.BooleanField(u"Published", default=False)
	comments_enabled = models.BooleanField(u"Comments Enabled", default=True)
	slug = models.SlugField(u"URL", max_length=100)

	def __unicode__(self):
		return self.title

	def published_comments(self):
		"Returns the published comments"
		return self.comments.filter(published=True).order_by("datetime")
	
	def get_full_url(self):
		site_url = Site.objects.get_current().domain
		dt = self.datetime
		if self.sticky == True:
			return ""
		return "http://%s/blog/%s/%s/" % (site_url, self.datetime.strftime("%Y/%m/%d"), self.slug)
	
	def get_datetime(self):
		return self.datetime.strftime("%d.%m.%Y @ %H:%M")

	get_datetime.short_description = "Event Published On"

	def get_entry_url(self):
		site_url = Site.objects.get_current().domain
		entry_url = "http://%s/blog/%s/%s/" % (site_url, self.datetime.strftime("%Y/%m/%d"), self.slug)
		if self.sticky == True:
			return ""
		return "<a href='%s' title='Click here to read the entry..' target='_blank'>%s</a>" % (entry_url, entry_url)
	
	get_entry_url.short_description = "URL of Entry"
	get_entry_url.allow_tags = True
	get_entry_url.admin_order_field = "-datetime"

	def delete_entry(self):
		url = "/admin/%s/%s/%s/delete/" % (self._meta.app_label, self._meta.module_name, self.id)
		return "<a href='%s' title='Click here to delete this entry'>Delete This Entry</a>" % url
	
	delete_entry.short_description = ""
	delete_entry.allow_tags = True

	class Meta:
		get_latest_by = "datetime"
		ordering = ["title"]
		verbose_name = "entry"
		verbose_name_plural = "entries"
