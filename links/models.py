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
from raptiye.tags.models import Tag

class LinkCategories(models.Model):
	'The model that stores the categories of the links..'
	title = models.CharField(u'Title', max_length='20')
	image = models.CharField(u'Image URL', max_length='200', help_text='(32x32)')
	level = models.IntegerField(u'Level', default=0)
	
	def __unicode__(self):
		return self.title
	
	def show_image(self):
		return "<img src='%s' title='preview of link category image..' style='margin-right: 10px;'> [%s]" % (self.image, self.image)
	show_image.allow_tags = True
	show_image.short_description = u'Image URL'
	
	class Meta:
		verbose_name = u'Link Category'
		verbose_name_plural = u'Link Categories'
		ordering = ['level', 'title']

class Links(models.Model):
	'The model that stores the links to outer web sites..'
	category = models.ForeignKey(LinkCategories, related_name='links', verbose_name=u'category')
	title = models.CharField(u'Title', max_length='50')
	description = models.CharField(u'Description', max_length='200', blank=True)
	url = models.URLField(u'URL')
	tags = models.ManyToManyField(Tag, verbose_name="tags", related_name="links")
	window = models.BooleanField(u'Open in new window', default=False)
	
	def __unicode__(self):
		return self.title
	
	def go_to_url(self):
		return "<a href='%s' title='click here to go to the url..'>%s</a>" % (self.url, self.url)
	go_to_url.allow_tags = True
	go_to_url.short_description = u'URL'
	
	def get_linked_category(self):
		return "<a href='?q=%s' title='click here to filter the links by this category..'>%s</a>" % (self.category, self.category)
	get_linked_category.allow_tags = True
	get_linked_category.short_description = u"Category"
	
	def get_tags_for_link(self):
		return ", ".join("<a href='?q=%s' title='click here to filter the links by this tag..'>%s</a>" % (tag.name, tag.name) for tag in self.tags.all())
	get_tags_for_link.allow_tags = True
	get_tags_for_link.short_description = u"Tags of Link"
	
	class Meta:
		verbose_name = u'Link'
		verbose_name_plural = u'Links'
		ordering = ['title',]