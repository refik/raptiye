# coding: utf-8
# 
# raptiye
# Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

from datetime import datetime

from raptiye.tags.models import Tag

class TagCloud():
	"""
	Defines the methods which will be used
	to construct the tag cloud..

	"""

	MIN_USED_TAG_COUNT = 0
	MAX_USED_TAG_COUNT = 0
	MAX_FONT_RANGE = 26
	MIN_FONT_RANGE = 10
	TAG_CLOUD = []
	debug = False

	def __init__(self, debug=False):
		self.construct_cloud()
		self.debug = debug
	
	def get_tag_cloud(self):
		if self.debug:
			print self.TAG_CLOUD
		return self.TAG_CLOUD

	def empty_tag_cloud(self):
		self.TAG_CLOUD = []

	def set_min_font_range(self, value):
		self.MIN_FONT_RANGE = value

	def get_min_font_range(self):
		return self.MIN_FONT_RANGE

	def get_max_font_range(self):
		return self.MAX_FONT_RANGE

	def set_max_font_range(self, value):
		self.MAX_FONT_RANGE = value

	def get_max_count(self):
		return self.MAX_USED_TAG_COUNT
	
	def set_max_count(self, value):
		self.MAX_USED_TAG_COUNT = value
	
	def get_min_count(self):
		return self.MIN_USED_TAG_COUNT

	def set_min_count(self, value):
		self.MIN_USED_TAG_COUNT = value
	
	def construct_cloud(self):
		# clearing tag cloud
		self.empty_tag_cloud()
		freq = []
		for tag in Tag.objects.all():
			if tag.entries.count() == 0:
				continue
			else:
				frequency = tag.entries.filter(published=True, datetime__lte=datetime.now())
				self.TAG_CLOUD.append({"name": tag.name, "slug": tag.slug,"font_size": frequency.count()})
				if self.debug:
					print "%s with count: %d" % (tag.name, frequency.count())
				freq.append(frequency.count())

		# control to take care when no tags exist..
		if freq.__len__() == 0:
			return None

		# find max and min values in freq.
		self.set_min_count(min(freq))
		self.set_max_count(max(freq))
		
		if self.debug:
			print "Min. Freq. Count: %d" % self.get_min_count()
			print "Max. Freq. Count: %d" % self.get_max_count()
		
		# calculate the rise value..
		rise = float((self.get_max_count() - self.get_min_count())) / float((self.get_max_font_range() - self.get_min_font_range()))
		
		if self.debug:
			print "Rise is: %f" % rise
		
		if rise != 0 and rise < 1:
			rise = 1/rise
		
		# updating the values of the dict by font sizes..
		for tag in self.TAG_CLOUD:
			# if tag count is equal to minimum, then set the font to the minimum
			if tag['font_size'] == self.get_min_count():
				tag['font_size'] = "%d%s" % (self.get_min_font_range(), "px")
			elif tag['font_size'] == self.get_max_count():
				tag['font_size'] = "%d%s" % (self.get_max_font_range(), "px")
			else:
				#font_rise = rise / (tag['font_size'] - self.get_min_count())
				font_rise = (tag['font_size'] - self.get_min_count()) / rise
				tag['font_size'] = "%d%s" % (self.get_min_font_range() + font_rise, "px")

