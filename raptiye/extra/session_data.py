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