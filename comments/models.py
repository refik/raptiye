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
from django.contrib.auth.models import User
from raptiye.blog.models import Entry

class Comments(models.Model):
	entry = models.ForeignKey(Entry, related_name='comments', verbose_name=u"Entry")
	author = models.ForeignKey(User, related_name='comments', verbose_name=u"Author")
	author_ip = models.IPAddressField(u"Author's IP", blank=True, null=True)
	# the following anonymous related fields are for comments that were before new raptiye..
	anonymous_author = models.CharField(u"Anonymous Author", blank=True, max_length=100)
	anonymous_author_email = models.EmailField(u"Anonymous Author E-Mail", blank=True, max_length=100)
	anonymous_author_web_site = models.CharField(u"Anonymous Author Web Site", blank=True, max_length=100)
	datetime = models.DateTimeField()
	content = models.TextField(u"Comment")
	published = models.BooleanField(u"Published", default=False)
	notification = models.BooleanField(u"Notification", default=False)
	
	def __unicode__(self):
		return "Comment for '" + self.entry.title + "' by " + self.author.username
	
	# overwriting the save method..
	def save(self, *args, **kwargs):
		web_site = self.anonymous_author_web_site
		# checking if the web site starts with http:// and adds it if there's none
		if len(web_site) and not web_site.startswith("http://") and not web_site.startswith("https://"):
			self.anonymous_author_web_site = "http://" + self.anonymous_author_web_site
		
		# saving the model
		super(Comments, self).save(*args, **kwargs)
	
	def get_entry_name(self):
		return self.entry.title
	
	get_entry_name.short_description = u"Entry Title"
	
	def get_entry_url(self):
		return u"<a href='%s' title='click here to see this blog entry..' target='_blank'>See Blog Entry</a>" % self.entry.get_full_url()
		
	get_entry_url.short_description = u"Entry URL"
	get_entry_url.allow_tags = True
	
	def get_datetime(self):
		return self.datetime.strftime("%d.%m.%Y @ %H:%M")
	
	get_datetime.short_description = u"Comment Written On"
	
	def get_author_info(self):
		un = self.author.username
		ue = self.author.email
		aun = self.anonymous_author
		aue = self.anonymous_author_email
		if un == "anonymous":
			return u"%s - <a href='mailto: %s' title='click here to send an e-mail to the user..'>%s</a>" % (aun, aue, aue)
		return u"%s - <a href='mailto: %s' title='click here to send an e-mail to the user..'>%s</a>" % (un, ue, ue)
	
	get_author_info.short_description = "User Info"
	get_author_info.allow_tags = True
	
	def get_author_web_site(self):
		ws = self.author.get_profile().web_site
		aws = self.anonymous_author_web_site
		if ws == "":
			if aws == "":
				return ""
			else:
				return u"<a href='%s' title='click here to visit the user\'s web site..' target='_blank'>%s</a>" % (aws, aws)
		return u"<a href='%s' title='click here to visit the user\'s web site..' target='_blank'>%s</a>" % (ws, ws)
	
	get_author_web_site.short_description = u"User Web Site"
	get_author_web_site.allow_tags = True
	
	class Meta:
		get_latest_by = "datetime"
		ordering = ["-datetime"]
		verbose_name = "Comment"
		verbose_name_plural = "Comments"
