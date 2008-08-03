#-*- encoding: utf-8 -*-

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

	def __init__(self, lang='tr'):
		self.construct_cloud(lang)
	
	def get_tag_cloud(self):
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
	
	def construct_cloud(self, lang='tr'):
		# clearing tag cloud
		self.empty_tag_cloud()
		freq = []
		for tag in Tag.objects.all():
			if tag.entries.count() == 0:
				continue
			else:
				entry_counter_for_language = tag.entries.filter(language=lang).count()
				if entry_counter_for_language > 0:
					self.TAG_CLOUD.append({"name": tag.name, "font_size": entry_counter_for_language})
					freq.append(entry_counter_for_language)

		# control to take care when no tags exist..
		if freq.__len__() == 0:
			return

		# find max and min values in freq.
		self.set_min_count(min(freq))
		self.set_max_count(max(freq))
		# calculate the rise value..
		rise = float((self.get_max_count() - self.get_min_count())) / float((self.get_max_font_range() - self.get_min_font_range()))
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
				font_rise = rise / (tag['font_size'] - self.get_min_count())
				tag['font_size'] = "%d%s" % (self.get_min_font_range() + font_rise, "px")
