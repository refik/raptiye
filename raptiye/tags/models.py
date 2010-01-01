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

from django.db import models

class Tag(models.Model):
	name = models.CharField(u"Tag Name", max_length=30, unique=True)
	slug = models.SlugField(u"URL", max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
		ordering = ["name"]

