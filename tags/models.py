#-*- encoding: utf-8 -*-

from django.db import models

class Tag(models.Model):
	name = models.CharField(u"Tag Name", max_length=30, unique=True)
	slug = models.SlugField(u"URL", max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
		ordering = ["name"]
