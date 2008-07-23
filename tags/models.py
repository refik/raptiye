#-*- encoding: utf-8 -*-

from django.db import models

class Tag(models.Model):
	name = models.CharField(u"Etiket İsmi", max_length=30, unique=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Etiket"
		verbose_name_plural = "Etiketler"
		ordering = ["name"]
