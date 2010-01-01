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

"""
Module that stores temporary data in the current session
After the data is reached within the template, the data is
removed completely.

This module is generally used for things like messaging
the users or distinguishing between posted forms..

"""

from django.utils.encoding import StrAndUnicode

def session_data(request):
	return {"session_data": LazySessionData(request)}

def create_data(request, key, value):
	"""
	Creates new data within the current session
	
	"""

	if hasattr(request, "session"):
		if request.session.has_key("data"):
			request.session["data"][key] = value
		else:
			request.session["data"] = {key: value}
	return False

def get_and_delete_data(request):
	"""
	Gets and deletes the data from the current session
	
	"""

	if hasattr(request, "session") and request.session.has_key("data"):
		return request.session.pop("data")
	return {}

class LazySessionData(StrAndUnicode):
	"""
	Lazy class that stores the data until needed..
	
	"""

	def __init__(self, request):
		self.request = request
	
	def __unicode__(self):
		return unicode(self.data)
	
	@property
	def data(self):
		if hasattr(self, "_data"):
			return self._data
		self._data = get_and_delete_data(self.request)
		return self._data

