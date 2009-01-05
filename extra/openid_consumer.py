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

"""
Module to handle all OpenID stuff..

Requires python-openid >= 2.0
"""

from django.contrib.auth.models import User
from django.db import connection
from raptiye.extra.exceptions import OpenIDDiscoveryError
from raptiye.extra.messages import OPENID_FAILURE_MESSAGE
from sqlite3 import OperationalError
from openid.consumer.consumer import Consumer, SUCCESS
from openid.consumer.discover import DiscoveryFailure
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.store.sqlstore import SQLiteStore

def openid_user_exists(identifier):
	if User.objects.filter(profile__openid=identifier):
		return True
	return False

class OpenID():
	"""
	Consumer class that interacts with the OpenID provider
	and authenticates the user..
	"""
	
	def __init__(self, request, link_on_success, link_on_fail):
		# making sure that the db connection is open
		connection.cursor()
		self._store = SQLiteStore(connection.connection)
		self._consumer = Consumer(request.session, self._store)
		self._realm = "http://%s" % request.get_host()
		self._required_extensions = ["nickname", "email", "fullname"]
		self.link_on_success = link_on_success
		self.link_on_fail = link_on_fail
	
	def _get_full_url(self, url):
		if not url.startswith("http://"):
			url = self._realm + url
		return url
	
	def _parse_response(self, response):
		"""
		parses the response and return a dict of
		parameters.. the dict will be returned to 
		the view to redirect the user to some specific
		page..
		
		only caring about SUCCESS since i classify all
		other statuses as failure.
		"""
		
		params = {}
		
		if response.status == SUCCESS:
			sreg_response = SRegResponse.fromSuccessResponse(response)
			
			params["identifier"] = response.identity_url
			params["user_info"] = {} if not sreg_response else sreg_response.data
			params["link"] = self.link_on_success
		else:
			params["message"] = OPENID_FAILURE_MESSAGE
			params["link"] = self.link_on_fail
		
		return params
	
	def authenticate(self, identifier, return_to):
		# constructing a full return to address
		return_to = self._get_full_url(return_to)
		
		try:
			self._auth = self._consumer.begin(identifier)
			if not openid_user_exists(identifier):
				self._auth.addExtension(SRegRequest(required=self._required_extensions))
		except OperationalError:
			# the openid store tables are not found, so create them
			# and redo everything..
			self._store.createTables()
			return self.authenticate(identifier, return_to)
		except DiscoveryFailure:
			raise OpenIDDiscoveryError
		provider_url = self._auth.redirectURL(realm=self._realm, return_to=return_to)
		return provider_url
	
	def complete(self, params, return_to):
		# constructing a full return to address
		return_to = self._get_full_url(return_to)
		openid_response = self._consumer.complete(params, return_to)
		return self._parse_response(openid_response)