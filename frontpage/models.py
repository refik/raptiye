#-*- encoding: utf-8 -*-

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
	title = models.CharField(u"Site Title", max_length=20, help_text="Required")
	title_html = models.CharField(u"Site Title (HTML)", max_length=200, help_text="The HTML representation of the title..")
	subtitle = models.CharField(u"Site Subtitle", max_length=80, help_text="Required")
	subtitle_html = models.CharField(u"Site Subtitle (HTML)", max_length=200, help_text="The HTML representation of the subtitle..")
	content_title = models.CharField(u"Content Title", max_length=100, blank=True, help_text="Optional.. HTML can also used..")
	content = models.TextField(u"Content Body", help_text="Required.. HTML can also be used..")
	rss_title = models.CharField(u"RSS Title", max_length=100, blank=True, help_text="Optional.. HTML can also used..")
	rss_url = models.CharField(u"RSS URL", max_length=200, blank=True, help_text="Optional.. HTML can also be used..")
	rss_limit = models.IntegerField(u"RSS News Limit", blank=True, default=5, help_text="Optional.. HTML can also be used..")
	footer = models.TextField(u"Footer", help_text="Footer of the Main Page.. HTML can be used..")
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
	page = models.ForeignKey(FrontPage)
	title = models.CharField(u"Link Name", core=True, max_length=30)
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
