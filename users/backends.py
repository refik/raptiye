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

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from raptiye.extra.exceptions import OpenIDUsernameExistsError

class OpenIDBackend:
	"""
	Plugs in OpenID support to Django's authentication
	framework.
	
	It simply looks for a user who has some certain OpenID
	identifier in his profile or creates a new user..
	
	The authentication method takes a dictionary that 
	contains necessary information to create the new user 
	such as username, e-mail address and full name.
	
	Password for new users is stored in settings.
	"""
	
	def _parse_fullname(self, fullname):
		"""
		Splits given fullname into tokens and assings all words
		upto the last one into the first name and the last one 
		info the surname..
		"""
		return (" ".join(fullname.split(" ")[:-1]), fullname.split(" ")[-1])
	
	def authenticate(self, identifier, user_info):
		user = None
		
		if isinstance(identifier, str) and isinstance(user_info, dict):
			try:
				user = User.objects.get(profile__openid=identifier)
			except User.DoesNotExist:
				# creating a new user with the user info
				if user_info.has_key("nickname") and user_info.has_key("email"):
					username = user_info["nickname"]
					password = settings.OPENID_PASSWORD_FOR_NEW_USER
					email = user_info["email"]
					user = User(username=username, password=password, email=email)
					if user_info.has_key("fullname"):
						user.first_name, user.last_name = self._parse_fullname(user_info["fullname"])
					# if there's already a user with that username, simply
					# redirect to the login page informing the user
					try:
						user.save()
						# creating user profile.. in order to create a profile
						# the user must be already created..
						user.profile.create()
						# associating openid identifier with the user
						profile = user.get_profile()
						profile.openids.create(identifier=identifier)
						profile.save()
					except IntegrityError:
						raise OpenIDUsernameExistsError
		return user
	
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None