#!/usr/bin/env python
# encoding: utf-8
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
initials.py

Does the necessary jobs after the initial installation of raptiye..
"""

from django.conf import settings
from django.contrib.auth.models import User
from raptiye.users.models import UserProfile

def create_anonymous_user():
	"""
	Creates the anonymous user that will be
	the new raptiye user of all comments that
	were entered earlier..
	"""
	if User.objects.filter(username="anonymous").count() == 0:
		user = User.objects.create_user("anonymous", settings.EMAIL_INFO_ADDRESS_TR)
		user.first_name = "Anonymous"
		user.last_name = "User"
		user.save()
		user.profile.create()

def create_profile_for_first_user():
	"""
	When a Django application is first created,
	it asks permission to create a user who has
	the administrator privileges. Usually this 
	user doesn't have a profile..
	
	This method creates the profile for that user.
	"""
	if User.objects.count() and not UserProfile.objects.count():
		user = User.objects.get(pk=1)
		user.profile.create()