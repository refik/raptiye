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

class FrontPage(models.Model):
	"""
	FrontPage Class

	This is the class that we hold everything about the
	frontpage.. It can be in Turkish and English with 
	respect to the choice list in settings.

	It's only logical if we create 1 frontpage for each
	language choice..!
	"""
	title = models.CharField(u"Site Title", max_length=20, help_text=u"Required")
	title_html = models.CharField(u"Site Title (HTML)", max_length=200, help_text=u"The HTML representation of the title..")
	title_link = models.URLField(u"Site Title Link", blank=True, null=True, verify_exists=False, max_length=200, help_text=u"This is the link of the title..")
	subtitle = models.CharField(u"Site Subtitle", max_length=80, help_text=u"Required")
	subtitle_html = models.CharField(u"Site Subtitle (HTML)", max_length=200, help_text=u"The HTML representation of the subtitle..")
	content_title = models.CharField(u"Content Title", max_length=100, blank=True, help_text=u"Optional.. HTML can also used..")
	content = models.TextField(u"Content Body", help_text=u"Required.. HTML can also be used..")
	rss_title = models.CharField(u"RSS Title", max_length=100, blank=True, help_text=u"Optional.. HTML can also used..")
	rss_url = models.CharField(u"RSS URL", max_length=200, blank=True, help_text=u"Optional.. HTML can also be used..")
	rss_limit = models.IntegerField(u"RSS News Limit", blank=True, default=10, help_text=u"Optional.. HTML can also be used..")
	footer = models.TextField(u"Footer", help_text=u"Footer of the Main Page.. HTML can be used..")
	language = models.CharField(u"Language", choices=settings.LANGUAGES, default="tr", max_length=2)

	def __unicode__(self):
		return u"%s - %s" % (self.title, self.subtitle)
	
	class Meta:
		verbose_name = u"FrontPage"
		verbose_name_plural = u"FrontPage"

class Links(models.Model):
	"""
	Links Class

	This is the class that we hold every link that's 
	accessible through frontpage. This class doesn't
	have any admin panel interface and only accessible
	via FrontPage interface.

	Usually there's no limit for creating links for the 
	frontpage. Because of the design limitations, creating
	only 4-5 links is adviced..!
	"""
	page = models.ForeignKey(FrontPage, related_name='links')
	title = models.CharField(u"Link Name", max_length=30)
	# url is defined as CharField since it doesn't accept urls like /blog
	url = models.CharField(u"URL", help_text="Can be relative link like /blog", max_length=20)
	image = models.ImageField(u"Image", upload_to="images/upload")
	target = models.BooleanField(u"External Link", default=False)
	level = models.IntegerField(u"Level", default=0, help_text="Used to move the link up and down..")

	def __unicode__(self):
		return u"%s (%s)" % (self.title, self.url)
	
	class Meta:
		ordering = ["level", "title"]
		verbose_name = u"Link"
		verbose_name_plural = u"Links"
