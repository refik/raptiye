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
from django.db import models

class UserProfile(models.Model):
	"""
	Stores additional information about the users..
	"""
	
	user = models.ForeignKey(User, related_name='profile', verbose_name=u"User")
	avatar = models.URLField(u"Avatar", default=settings.DEFAULT_AVATAR)
	web_site = models.URLField(u"Web Site", blank=True)
	activation_key = models.CharField(u"Aktivasyon Kodu", max_length=100, blank=True)
	last_modified = models.DateTimeField(u"Last Modified Date", auto_now=True)
	
	def __unicode__(self):
		return "User Profile of %s" % self.user.username

	class Meta:
		verbose_name = u"User Profile"
		verbose_name_plural = u"User Profiles"

class OpenID(models.Model):
	"Model to associate OpenID's with Users' Profile"
	
	profile = models.ForeignKey(UserProfile, related_name="openids", verbose_name="OpenID Identifier(s)", null=True)
	identifier = models.URLField(u"OpenID Identifier", unique=True)
	
	def __unicode__(self):
		return "OpenID Identifier (%s)" % self.identifier
	
	class Meta:
		verbose_name = u"OpenID Identifier"
		verbose_name_plural = u"OpenID Identifiers"