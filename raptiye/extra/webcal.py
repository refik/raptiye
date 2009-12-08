#!/usr/bin/env python
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

import calendar

class WebCalendar():
	"""
	creates a web calendar that can be bound to
	some objects if the object has a datetime field.
	"""

	def __init__(self, year, month, day, object=None, datetime_field='', locale=''):
		self.year = year
		self.month = month
		self.day = day
		self.object = object
		self.datetime_field = datetime_field
		if not locale:
			self.calendar = calendar.LocaleTextCalendar()
		else:
			self.calendar = calendar.LocaleTextCalendar(0, locale)
			
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

	def set_object(self, object):
		self.object = object
	
	def set_datetime_field(self, datetime_field):
		self.datetime_field = datetime_field
	
	def render(self, table_id="", link_path="", link_title="", link_class=""):
		html = u"<table id='%s'>" % table_id
		# creating the header part
		html += u"<tr>"
		# printing days' name 3 chars long
		for i in range(7):
			html += u"<th>%s</th>" % self.calendar.formatweekday(i, 3).lower()
		html += u"</tr>"
		# creating the rest of the table
		for week in self.calendar.monthdayscalendar(self.get_year(), self.get_month()):
			html += u"<tr>"
			for day in week:
				if day == 0:
					html += u"<td></td>"
				else:
					if self.get_object() is not None and self.get_datetime_field() is not None:
						filters = {
							self.get_datetime_field() + "__year": self.get_year(),
							self.get_datetime_field() + "__month": self.get_month(),
							self.get_datetime_field() + "__day": day,
						}
						if self.get_object().filter(**filters).count() > 0:
							if day == self.get_day():
								html += u"<td class='today'><a href='%s/%4d/%02d/%02d/' title='%s' class='%s'>%d</a></td>" % (link_path, self.get_year(), 
									self.get_month(), day, link_title, link_class, day)
							else:
								html += u"<td><a href='%s/%4d/%02d/%02d/' title='%s' class='%s'>%d</a></td>" % (link_path, self.get_year(), 
									self.get_month(), day, link_title, link_class, day)
						else:
							if day == self.get_day():
								html += u"<td class='today'>%d</td>" % day
							else:
								html += u"<td>%d</td>" % day
					else:
						if day == self.get_day():
							html += u"<td class='today'>%d</td>" % day
						else:
							html += u"<td>%d</td>" % day
			html += u"</tr>"
		html += u"</table>"
		return html
