from django.db import models

class LinkCategories(models.Model):
	'The model that stores the categories of the links..'
	title = models.CharField(u'Title', max_length='20')
	image = models.CharField(u'Image URL', max_length='200', help_text='(32x32)')
	level = models.IntegerField(u'Level', default=0)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name = u'Link Category'
		verbose_name_plural = u'Link Categories'
		ordering = ['level', 'title']

class Links(models.Model):
	'The model that stores the links to outer web sites..'
	category = models.ForeignKey(LinkCategories, verbose_name=u'Category')
	title = models.CharField(u'Title', max_length='50')
	url = models.URLField(u'URL')
	window = models.BooleanField(u'Open in new window', default=False)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name = u'Link'
		verbose_name_plural = u'Links'
		ordering = ['title',]