#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import calendar

class WebCalendar():
	"""
	creates a web calendar that can be bound to
	some objects if the object has a datetime field.
	"""

	def __init__(self, year, month, day, object=None, datetime_field='', locale='', lang_field='', lang='tr'):
		self.year = year
		self.month = month
		self.day = day
		self.object = object
		self.datetime_field = datetime_field
		if locale == '':
			self.calendar = calendar.LocaleTextCalendar()
		else:
			self.calendar = calendar.LocaleTextCalendar(0, locale)
		self.lang_field = lang_field
		self.lang = lang
	
	def get_lang_field(self):
		return self.lang_field
	
	def get_lang(self):
		return self.lang
	
	def get_year(self):
		return self.year

	def get_month(self):
		return self.month

	def get_day(self):
		return self.day
	
	def get_object(self):
		return self.object

	def get_datetime_field(self):
		return self.datetime_field
	
	def render(self, table_id="", link_path="", link_title="", link_class=""):
		html = "<table id='%s'>" % table_id
		# creating the header part
		html += "<tr>"
		# printing days' name 3 chars long
		for i in range(7):
			html += "<th>%s</th>" % self.calendar.formatweekday(i, 3).lower()
		html += "</tr>"
		# creating the rest of the table
		for week in self.calendar.monthdayscalendar(self.get_year(), self.get_month()):
			html += "<tr>"
			for day in week:
				if day == 0:
					html += "<td></td>"
				else:
					if self.get_object() is not None and self.get_datetime_field() is not None:
						filters = {
							self.get_datetime_field() + "__year": self.get_year(),
							self.get_datetime_field() + "__month": self.get_month(),
							self.get_datetime_field() + "__day": day,
							self.get_lang_field(): self.get_lang(),
						}
						if self.get_object().objects.filter(**filters).count() > 0:
							if day == self.get_day():
								html += "<td class='today'><a href='%s/%d/%d/%d/' title='%s' class='%s'>%d</a></td>" % (link_path, self.get_year(), 
										self.get_month(), day, link_title, link_class, day)
							else:
								html += "<td><a href='%s/%d/%d/%d/' title='%s' class='%s'>%d</a></td>" % (link_path, self.get_year(), 
										self.get_month(), day, link_title, link_class, day)
						else:
							if day == self.get_day():
								html += "<td class='today'>%d</td>" % day
							else:
								html += "<td>%d</td>" % day
					else:
						if day == self.get_day():
							html += "<td class='today'>%d</td>" % day
						else:
							html += "<td>%d</td>" % day
			html += "</tr>"
		html += "</table>"
		return html
