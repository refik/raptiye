#-*- encoding: utf-8 -*-
# raptiye
# Copyright (C)  Alper KANAT  <alperkanat@raptiye.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
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
	
	def get_relative_url(self):
		return "%s%s/%s/" % (reverse("blog"), self.datetime.strftime("%Y/%m/%d"), self.slug)
	
	def get_full_url(self):
		site_url = Site.objects.get_current().domain
		return "http://%s%s" % (site_url, self.get_relative_url())
	
	def get_datetime(self):
		return self.datetime.strftime("%d.%m.%Y @ %H:%M")
	
	get_datetime.short_description = "Event Published On"
	
	def get_entry_url(self):
		entry_url = self.get_relative_url()
		return "<a href='%s' title='Click here to read the entry..' target='_blank'>%s</a>" % (entry_url, entry_url)
	
	get_entry_url.short_description = "URL of Entry"
	get_entry_url.allow_tags = True
	get_entry_url.admin_order_field = "-datetime"
	
	def delete_entry(self):
		url = "/admin/%s/%s/%s/delete/" % (self._meta.app_label, self._meta.module_name, self.id)
		return "<a href='%s' title='Click here to delete this entry'>Delete This Entry</a>" % url
	
	delete_entry.short_description = ""
	delete_entry.allow_tags = True
	
	def get_previous_post(self):
		return Entry.objects.filter(published=True, id__lt=self.id).latest()
	
	def get_next_post(self):
		return Entry.objects.filter(published=True, id__gt=self.id).reverse().latest()
	
	class Meta:
		get_latest_by = "datetime"
		ordering = ["title"]
		verbose_name = "entry"
		verbose_name_plural = "entries"